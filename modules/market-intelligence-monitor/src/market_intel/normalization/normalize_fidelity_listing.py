from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional


PRESS_URL_RE = re.compile(
    r"^https://newsroom\.fidelity\.com/pressreleases/[^\"'\s<>]+$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Candidate:
    url: str
    title: str | None
    date_text: str | None


def _load_raw(raw_path: Path) -> dict[str, Any]:
    data = json.loads(raw_path.read_text(encoding="utf-8"))
    if data.get("schema") != "raw_signal.v0":
        raise ValueError(f"Unexpected schema in {raw_path}: {data.get('schema')}")
    return data


def _maybe_fix_mojibake(text: str) -> str:
    """
    Best-effort repair for common UTF-8-as-latin1 mojibake (Â®, â€™, â„¢, etc.).
    We ONLY attempt repair when we see telltale characters, and we fall back safely.
    """
    if not text:
        return text

    # Heuristic triggers: common mojibake markers.
    if ("Â" not in text) and ("â" not in text):
        return text

    # Attempt: interpret current string as latin-1 bytes then decode as UTF-8.
    # If it was already correct, this usually makes it worse; hence the trigger above.
    try:
        repaired = text.encode("latin-1", errors="strict").decode("utf-8", errors="strict")
        # Guardrail: only accept if it *reduces* mojibake markers.
        if repaired.count("Â") + repaired.count("â") < text.count("Â") + text.count("â"):
            return repaired
    except Exception:
        pass

    return text


def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


class _FidelityListingParser(HTMLParser):
    """
    DOM-scoped (streaming) parser:
      - when we see an <a href="press-url">TITLE</a>, we start a candidate
      - when we see the next <div class="news-log">DATE</div>, we attach it
    This preserves page order and avoids global sorting / index pairing.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.candidates: list[Candidate] = []

        # Current candidate under construction
        self._cur_url: Optional[str] = None
        self._cur_title_parts: list[str] = []
        self._cur_date_parts: list[str] = []

        # State flags
        self._in_a = False
        self._in_date_div = False

        # For rare layouts where date appears before link in the same item
        self._pending_date_text: Optional[str] = None

        # Dedup by URL while preserving encounter order
        self._seen_urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag_l = tag.lower()
        attrs_d = {k.lower(): (v or "") for k, v in attrs}

        if tag_l == "a":
            href = attrs_d.get("href", "").strip()
            if href and PRESS_URL_RE.match(href):
                # If we already have an unfinished candidate (no date found), flush it.
                self._flush_candidate()

                # Start new candidate
                self._cur_url = href
                self._cur_title_parts = []
                self._cur_date_parts = []
                self._in_a = True

        elif tag_l == "div":
            cls = attrs_d.get("class", "")
            # Fidelity uses <div class="news-log">December 11, 2025</div>
            if "news-log" in cls.split() or "news-log" in cls:
                self._in_date_div = True
                self._cur_date_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag_l = tag.lower()

        if tag_l == "a" and self._in_a:
            self._in_a = False

            # If we have a title, normalize it now
            if self._cur_title_parts:
                title = _norm_space("".join(self._cur_title_parts))
                self._cur_title_parts = [title]

            # If a date was seen earlier (date-before-link layout), attach it now.
            if self._pending_date_text and self._cur_url and not self._cur_date_parts:
                self._cur_date_parts = [self._pending_date_text]
                self._pending_date_text = None

        elif tag_l == "div" and self._in_date_div:
            self._in_date_div = False
            date_text = _norm_space("".join(self._cur_date_parts))

            if date_text:
                # If we already have an active candidate, attach to it; otherwise hold pending.
                if self._cur_url:
                    self._cur_date_parts = [date_text]
                    # Often date comes after title; once we have both, flush.
                    self._flush_candidate()
                else:
                    # Date occurred before we saw the link/title; store as pending.
                    self._pending_date_text = date_text

    def handle_data(self, data: str) -> None:
        if not data:
            return
        if self._in_a and self._cur_url:
            self._cur_title_parts.append(data)
        elif self._in_date_div:
            self._cur_date_parts.append(data)

    def _flush_candidate(self) -> None:
        if not self._cur_url:
            return

        url = self._cur_url.strip()
        if url in self._seen_urls:
            # Reset state for duplicate encounters
            self._cur_url = None
            self._cur_title_parts = []
            self._cur_date_parts = []
            self._in_a = False
            return

        raw_title = _norm_space("".join(self._cur_title_parts)) if self._cur_title_parts else None
        raw_date = _norm_space("".join(self._cur_date_parts)) if self._cur_date_parts else None

        title = _maybe_fix_mojibake(raw_title) if raw_title else None
        date_text = _maybe_fix_mojibake(raw_date) if raw_date else None

        self.candidates.append(Candidate(url=url, title=title, date_text=date_text))
        self._seen_urls.add(url)

        # Reset candidate state
        self._cur_url = None
        self._cur_title_parts = []
        self._cur_date_parts = []
        self._in_a = False


def normalize_fidelity_press_listing(raw_path: Path, out_dir: Path) -> Path:
    raw = _load_raw(raw_path)
    html: str = raw.get("raw_content", "")

    parser = _FidelityListingParser()
    parser.feed(html)
    parser.close()

    candidates = parser.candidates

    out = {
        "schema": "normalized_signal.v0",
        "source_id": raw["source"]["id"],
        "fetched_at_utc": raw["fetch"]["fetched_at_utc"],
        "input_raw_path": str(raw_path),
        "candidate_count": len(candidates),
        "candidates": [c.__dict__ for c in candidates],
        "notes": "Normalization v0: DOM-scoped extraction from listing HTML (streaming HTMLParser). Titles/dates paired in encounter order; includes best-effort mojibake repair.",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (raw_path.stem.replace("__", "__normalized__") + ".json")
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path

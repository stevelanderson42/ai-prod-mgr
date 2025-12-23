from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PRESS_URL_RE = re.compile(
    r"https://newsroom\.fidelity\.com/pressreleases/[^\"'\s<>]+",
    re.IGNORECASE,
)

# Title appears as: <a href="PRESS_URL" ...>TITLE</a>
TITLE_BY_URL_RE_TEMPLATE = r'<a[^>]+href="{url_escaped}"[^>]*>(?P<title>[^<]+)</a>'

# Date appears as: <div class="news-log">December 11, 2025</div>
DATE_RE = re.compile(r'<div class="news-log">\s*([^<]+?)\s*</div>', re.IGNORECASE)


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


def normalize_fidelity_press_listing(raw_path: Path, out_dir: Path) -> Path:
    raw = _load_raw(raw_path)
    html: str = raw.get("raw_content", "")

    # 1) collect unique press URLs
    urls = sorted(set(PRESS_URL_RE.findall(html)))

    # 2) collect dates in order (best-effort)
    dates = DATE_RE.findall(html)
    # We'll map candidates to dates by index as a v0 heuristic.
    # Not perfect, but tends to be stable on list pages.

    candidates: list[Candidate] = []
    for i, url in enumerate(urls):
        # find the first anchor text for that URL
        url_escaped = re.escape(url)
        title_re = re.compile(TITLE_BY_URL_RE_TEMPLATE.format(url_escaped=url_escaped), re.IGNORECASE)
        m = title_re.search(html)
        title = m.group("title").strip() if m else None

        date_text = dates[i].strip() if i < len(dates) else None

        candidates.append(Candidate(url=url, title=title, date_text=date_text))

    out = {
        "schema": "normalized_signal.v0",
        "source_id": raw["source"]["id"],
        "fetched_at_utc": raw["fetch"]["fetched_at_utc"],
        "input_raw_path": str(raw_path),
        "candidate_count": len(candidates),
        "candidates": [c.__dict__ for c in candidates],
        "notes": "Normalization v0: regex extraction from listing HTML. Titles/dates are best-effort.",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (raw_path.stem.replace("__", "__normalized__") + ".json")
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import requests
import yaml


def _project_root() -> Path:
    p = Path(__file__).resolve()
    while p.name != "market-intelligence-monitor":
        p = p.parent
    return p



def _load_sources(config_path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "sources" not in data:
        raise ValueError(f"Invalid sources.yaml: expected top-level dict with 'sources'. path={config_path}")
    return data


def fetch_one(source_id: str) -> Path:
    root = _project_root()
    cfg = _load_sources(root / "config" / "sources.yaml")

    sources = cfg.get("sources", [])
    src = next((s for s in sources if s.get("id") == source_id), None)
    if not src:
        known = [s.get("id") for s in sources]
        raise ValueError(f"Unknown source_id={source_id}. Known IDs: {known}")

    url = src["url"]
    headers = {
        "User-Agent": "market-intelligence-monitor/0.1 (+learning project)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    resp = requests.get(url, headers=headers, timeout=30)
    fetched_at = datetime.now(timezone.utc).isoformat()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    evidence_dir = root / "data" / "evidence" / "raw"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    out_path = evidence_dir / f"{source_id}__{ts}.json"

    record = {
        "schema": "raw_signal.v0",
        "source": {
            "id": src.get("id"),
            "name": src.get("name"),
            "class": src.get("class"),
            "tier": src.get("tier"),
            "method": src.get("method"),
            "url": url,
        },
        "fetch": {
            "fetched_at_utc": fetched_at,
            "status_code": resp.status_code,
            "content_type": resp.headers.get("Content-Type", ""),
            "response_bytes": len(resp.content),
        },
        # Raw, as-is
        "raw_content": resp.text,
    }

    out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return out_path


def fetch_one_from_env(default_source_id: str = "fidelity_press") -> Path:
    source_id = os.getenv("MARKET_INTEL_SOURCE_ID", default_source_id).strip()
    return fetch_one(source_id)


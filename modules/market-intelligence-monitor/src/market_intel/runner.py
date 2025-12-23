from __future__ import annotations

from pathlib import Path

from market_intel.ingestion.fetch_one import fetch_one_from_env
from market_intel.normalization.normalize_fidelity_listing import normalize_fidelity_press_listing


def run() -> int:
    raw_path = Path(fetch_one_from_env())
    print("Ingestion OK")
    print(f"Evidence written: {raw_path}")

    # v0 normalization for fidelity listing pages
    norm_path = normalize_fidelity_press_listing(
        raw_path=raw_path,
        out_dir=raw_path.parent.parent / "normalized",
    )
    print("Normalization OK")
    print(f"Normalized written: {norm_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

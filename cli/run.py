from __future__ import annotations
import argparse, sys
import pandas as pd
from modules.utils import ensure_ts
from modules.patterns import load_patterns
from modules.rule_engine import run_rules
from modules.llm_engine import analyze_with_llm

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run fault detection on a CSV using rules or LLM")
    ap.add_argument("--data", required=True, help="CSV with at least 'ts' and feature columns")
    ap.add_argument("--plant-id", required=False, help="Overrides plant_id in output")
    ap.add_argument("--asset-id", required=False, help="Overrides asset_id in output")
    ap.add_argument("--patterns", required=True, help="YAML describing faults")
    ap.add_argument("--mode", choices=["rules","llm"], default="rules")
    ap.add_argument("--out", required=True, help="Output CSV for detected fault intervals")
    args = ap.parse_args()

    df = pd.read_csv(args.data)
    df = ensure_ts(df)
    patterns = load_patterns(args.patterns)

    # Plant/asset defaults (optional)
    plant_id = args.plant_id or patterns.get("defaults", {}).get("plant_id", "unknown_plant")
    asset_id = args.asset_id or patterns.get("defaults", {}).get("asset_id", "unknown_asset")

    if args.mode == "rules":
        res = run_rules(df, patterns, plant_id, asset_id)
    else:
        res = analyze_with_llm(df, patterns, plant_id, asset_id)

    res.to_csv(args.out, index=False)
    print(f"[run] wrote {len(res)} intervals → {args.out}")

from __future__ import annotations
import argparse, json, sys
import pandas as pd
from modules.timestream_fetch import fetch_timeseries
from modules.metadata_fetch import get_connection_for_plant

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Fetch telemetry from Timestream and save to CSV")
    ap.add_argument("--plant-id", required=True)
    ap.add_argument("--asset-id", required=True)
    ap.add_argument("--start", required=True, help="ISO8601")
    ap.add_argument("--end", required=True, help="ISO8601")
    ap.add_argument("--query", required=False, help="Optional raw query string")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    conn = get_connection_for_plant(args.plant_id)
    df = fetch_timeseries(args.plant_id, args.asset_id, args.start, args.end, query=args.query, connection=conn)
    df.to_csv(args.out, index=False)
    print(f"[fetch_data] wrote {len(df)} rows → {args.out}")

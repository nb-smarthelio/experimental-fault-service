from __future__ import annotations
import argparse, json
from modules.metadata_fetch import get_plant, get_connection_for_plant

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Fetch plant metadata and connection info")
    ap.add_argument("--plant-id", required=True)
    ap.add_argument("--out", required=False, help="Path to write JSON (optional)")
    args = ap.parse_args()

    plant = get_plant(args.plant_id)
    conn = get_connection_for_plant(args.plant_id)
    payload = {"plant": plant, "connection": conn}
    if args.out:
        import pathlib, json
        pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"[fetch_metadata] wrote → {args.out}")
    else:
        print(json.dumps(payload, indent=2))

from __future__ import annotations
from typing import Dict, Any, List
import pandas as pd

def _find_intervals(mask: pd.Series, ts: pd.Series, min_points: int = 1) -> List[tuple[str, str]]:
    # Identify contiguous True runs; return [(start_iso, end_iso)]
    mask = mask.fillna(False).astype(bool).reset_index(drop=True)
    ts = pd.to_datetime(ts).reset_index(drop=True)
    intervals = []
    run_start = None
    run_len = 0
    for i, ok in enumerate(mask):
        if ok:
            run_len += 1
            if run_start is None:
                run_start = ts[i]
        else:
            if run_len >= min_points and run_start is not None:
                intervals.append((run_start.isoformat(), ts[i-1].isoformat()))
            run_start = None
            run_len = 0
    if run_len >= min_points and run_start is not None:
        intervals.append((run_start.isoformat(), ts[len(ts)-1].isoformat()))
    return intervals

def run_rules(df: pd.DataFrame, patterns: Dict[str, Any], plant_id: str, asset_id: str) -> pd.DataFrame:
    """
    patterns format (see patterns/faults.yml):

    faults:
      - id: grid_curtailment_v1
        description: "High irradiance but curtailed AC power"
        condition: "irradiance_wm2 >= 600 and ac_power_kw < 80"  # pandas.eval expression
        min_points: 3   # consecutive points required
    """
    results = []
    df = df.copy()
    if "ts" not in df.columns:
        raise KeyError("DataFrame must contain 'ts' column (timestamps).")
    for f in patterns.get("faults", []):
        cond_expr = f.get("condition")
        if not cond_expr:
            continue
        min_points = int(f.get("min_points", 1))
        try:
            mask = pd.eval(cond_expr, engine="python", parser="pandas", local_dict=df.to_dict(orient="series"))
        except Exception as e:
            raise ValueError(f"Bad condition expression for fault '{f.get('id')}': {cond_expr} ⇒ {e}")
        intervals = _find_intervals(mask, df["ts"], min_points=min_points)
        for (start_iso, end_iso) in intervals:
            results.append({
                "plant_id": plant_id,
                "asset_id": asset_id,
                "fault_type": f.get("id", "unknown_fault"),
                "start_ts": start_iso,
                "end_ts": end_iso,
                "confidence": f.get("confidence", 0.9),
                "evidence": cond_expr
            })
    return pd.DataFrame(results)

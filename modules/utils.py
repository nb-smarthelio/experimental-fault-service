from __future__ import annotations
import pandas as pd

def ensure_ts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "ts" not in df.columns:
        raise KeyError("Expected a 'ts' column in the input data.")
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    return df

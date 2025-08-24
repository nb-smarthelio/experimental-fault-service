"""
LLM analyzer (optional).

Intended usage:
- Convert pattern descriptions + an aggregated data window into a prompt
- Call your LLM provider (OpenAI, Bedrock, etc.) to detect likely fault intervals
- Return a DataFrame with same schema as rule_engine.run_rules()

This is a stub with a deterministic fallback so the pipeline runs without keys.
"""
from __future__ import annotations
from typing import Dict, Any
import pandas as pd

def analyze_with_llm(df: pd.DataFrame, patterns: Dict[str, Any], plant_id: str, asset_id: str) -> pd.DataFrame:
    # TODO: Replace with real LLM call (provider SDK) and post-processing.
    # For now, return empty (no LLM decisions) so pipeline remains deterministic.
    return pd.DataFrame(columns=["plant_id","asset_id","fault_type","start_ts","end_ts","confidence","evidence"])

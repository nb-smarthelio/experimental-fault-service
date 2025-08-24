from __future__ import annotations
from typing import List, Dict, Any
import yaml, pathlib

def load_patterns(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict) and "faults" in data, "patterns file must have top-level 'faults' list"
    return data

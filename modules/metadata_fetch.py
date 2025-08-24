"""
Metadata fetcher — thin wrapper for your metadata service.
"""
from __future__ import annotations
from typing import Dict, Any

# Example: replace with actual helio code
# from heliolib.metadata_extraction_service.client import get_plant, get_connection_for_plant

def get_plant(plant_id: str) -> Dict[str, Any]:
    return {"plant_id": plant_id, "assets": [{"asset_id": "inv_7", "type": "inverter"}]}

def get_connection_for_plant(plant_id: str) -> Dict[str, Any]:
    return {"region": "ap-south-1", "timestream_db": "solar_prod", "timestream_table": "telemetry"}

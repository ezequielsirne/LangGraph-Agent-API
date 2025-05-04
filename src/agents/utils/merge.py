    # src/agents/utils/merge.py
"""
Utility helpers for combining partial results produced by parallel nodes.
"""

from typing import Dict, Any, List


def merge_parallel_results(results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Flatten outputs from `info_node` and `availability_node` while preserving
    non‑empty data from both.

    Parameters
    ----------
    results : dict
        {
          "info_node": {"retrieved_documents": [...]},
          "availability_node": {"availability": {...}, "retrieved_documents": [...]}
        }

    Returns
    -------
    dict
        {
          "retrieved_documents": [...],
          "availability": {...}
        }
    """

    merged: Dict[str, Any] = {}

    def _merge_payload(payload: Dict[str, Any]):
        for key, value in payload.items():

            # If key not present and value is truthy → copy
            if key not in merged:
                if value not in (None, [], {}):
                    merged[key] = value
                continue

            existing = merged[key]

            # Lists → concatenate sin duplicados
            if isinstance(existing, list) and isinstance(value, list):
                if value:  # new list not empty
                    merged[key] = existing + [x for x in value if x not in existing]

            # Dicts → shallow update, new dict prevalece en colisiones
            elif isinstance(existing, dict) and isinstance(value, dict):
                if value:
                    merged[key] = {**existing, **value}

            # Escalares → sobrescribe solo si el nuevo es truthy
            else:
                if value not in (None, "", 0):
                    merged[key] = value

    # Procesar info primero, availability después
    _merge_payload(results.get("info_node", {}) or {})
    _merge_payload(results.get("availability_node", {}) or {})

    return merged

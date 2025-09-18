# Updated on 2025-09-18 to confirm Git sync

import pandas as pd
from typing import Dict, Any, List

def classify_column(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "temporal"

    dtype = str(series.dtype)
    unique_vals = series.nunique()

    if dtype == "object":
        return "categorical (nominal)"
    elif dtype in ["int64", "float64"]:
        if unique_vals <= 10 and series.dropna().is_monotonic_increasing:
            return "categorical (ordinal)"
        else:
            return "continuous"
    else:
        return "unknown"

def classify_sheet_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = payload.get("data", {})
    dependent = payload.get("dependent_variable")

    if not data or dependent not in data:
        raise ValueError("Payload must include 'data' and a valid 'dependent_variable'")

    df = pd.DataFrame(data)

    # Coerce numeric and datetime types
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col], errors="raise")
            except:
                pass

    results: List[Dict[str, Any]] = []
    for col in df.columns:
        if col == dependent:
            continue

        classification = classify_column(df[col])
        dtype_label = "datetime" if pd.api.types.is_datetime64_any_dtype(df[col]) else str(df[col].dtype)

        base_row = {
            "column": col,
            "dtype": dtype_label,
            "unique_values": int(df[col].nunique()),
            "missing_values": int(df[col].isna().sum()),
            "classification": classification
        }

        if classification.startswith("categorical"):
            value_counts = df[col].value_counts(dropna=True)
            for idx, (label, count) in enumerate(value_counts.items()):
                row = base_row.copy() if idx == 0 else {
                    "column": "",
                    "dtype": "",
                    "unique_values": "",
                    "missing_values": "",
                    "classification": ""
                }
                row["value_counts"] = f'{count} "{label}"'
                results.append(row)
        else:
            base_row["value_counts"] = ""
            results.append(base_row)

    results.sort(key=lambda x: x["classification"])

    return {
        "dependent_variable": dependent,
        "dependent_stats": {
            "dtype": str(df[dependent].dtype),
            "unique_values": int(df[dependent].nunique()),
            "missing_values": int(df[dependent].isna().sum())
        },
        "independent_variables": results
    }
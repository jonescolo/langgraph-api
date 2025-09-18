import pandas as pd

def classify_column(series: pd.Series) -> str:
    dtype = str(series.dtype)
    unique_vals = series.nunique()

    if dtype == "object":
        return "categorical (nominal)"
    elif dtype in ["int64", "float64"]:
        if unique_vals <= 10:
            return "categorical (ordinal)"
        else:
            return "continuous"
    else:
        return "unknown"

def classify_sheet_payload(payload: dict) -> dict:
    df = pd.DataFrame(payload["data"])
    dependent = payload["dependent_variable"]

    # Coerce numeric types where possible
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    results = []
    for col in df.columns:
        if col == dependent:
            continue
        results.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "unique_values": int(df[col].nunique()),
            "missing_values": int(df[col].isna().sum()),
            "classification": classify_column(df[col])
        })

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
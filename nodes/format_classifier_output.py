def format_classifier_output(payload):
    raw = payload.get("independent_variables", [])
    grouped = {}
    current = None

    for item in raw:
        if "column" in item and item["column"]:
            current = item["column"]
            grouped[current] = {
                "name": current,
                "dtype": item.get("dtype", ""),
                "unique_values": item.get("unique_values", 0),
                "missing_values": item.get("missing_values", 0),
                "classification": item.get("classification", ""),
                "type": infer_type(current),
                "value_counts": []
            }
        elif "value_counts" in item and current:
            grouped[current]["value_counts"].append(item["value_counts"])

    return {"columns": list(grouped.values())}

def infer_type(col_name):
    col_name = col_name.lower()
    if "date" in col_name:
        return "date"
    elif "price" in col_name or "amount" in col_name:
        return "currency"
    elif "sqft" in col_name or "squarefeet" in col_name:
        return "area"
    elif "year" in col_name:
        return "year"
    else:
        return "general"
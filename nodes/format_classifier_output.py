def format_classifier_output(payload: dict) -> dict:
    columns = []
    current_column = None

    for item in payload.get("independent_variables", []):
        if "column" in item:
            current_column = {
                "name": item["column"],
                "dtype": item.get("dtype", ""),
                "unique_values": item.get("unique_values", 0),
                "missing_values": item.get("missing_values", 0),
                "classification": item.get("classification", ""),
                "type": item.get("type", "general"),
                "value_counts": []
            }
            columns.append(current_column)
        elif "value_counts" in item and current_column:
            current_column["value_counts"].append(item["value_counts"])

    return {"columns": columns}
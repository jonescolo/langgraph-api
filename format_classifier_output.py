def format_classifier_output(payload):
    raw = payload["independent_variables"]
    grouped = {}
    current = None

    for item in raw:
        if "column" in item and item["column"]:
            current = item["column"]
            grouped[current] = {
                "meta": {
                    "column": current,
                    "dtype": item["dtype"],
                    "unique_values": item["unique_values"],
                    "missing_values": item["missing_values"],
                    "classification": item["classification"]
                },
                "value_counts": []
            }
        elif "value_counts" in item and current:
            grouped[current]["value_counts"].append(item["value_counts"])

    return {"columns": list(grouped.values())}
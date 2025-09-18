import json
from classifier_node import classify_sheet_payload

# Load the test payload
with open("testdata.json", "r") as f:
    payload = json.load(f)

# Run the classifier
result = classify_sheet_payload(payload)

# Pretty-print the output
import pprint
pprint.pprint(result, sort_dicts=False)
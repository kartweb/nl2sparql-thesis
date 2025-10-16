import json
import sys

file_path = "data/nl2sparql_pairs.json"

with open(file_path, 'r') as f:
    data = json.load(f)

cleaned_data = [
    {k: item[k] for k in ("nl", "nl_keywords", "sparql") if k in item}
    for item in data
]

with open(file_path, 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print("Cleared everything but nl and sparql k:v")
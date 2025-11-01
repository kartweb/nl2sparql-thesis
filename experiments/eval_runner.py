#Must include prefix: 
#Must include graph name: 

import json
import os
def make_prompt(entry, fields):
    prefix = entry.get("prefix", "")
    graph = entry.get("graph", "")
    nl = entry.get("nl", "")

    # Always inclue these
    lines = [
        "Generate only SPARQL for NL qs using RAG when needed.",
        f"NL \"{nl}\"",
        "RAG",
        f"Shorten prefixes when possible",
        f"#Must include prefix: {prefix}",
        f"#Must include graph GRAPH (GRAPH must be under where block): {graph}"
    ]

    # Add only requested fields if they exist
    for key in fields:
        if key in entry:
            val = entry[key]
            if isinstance(val, (list, dict)):
                # json dumps converts a python objct into a JSON formatted string
                val = json.dumps(val, ensure_ascii=False, indent=2)
                lines.append(f"\"{key}\": {val},")
            else:
                lines.append(f"\"{key}\": \"{val}\",")

    return "\n".join(lines) + "\n---\n"

def main():
    idx = 1
    options = ["retrieved_terms", "retrieved_embeddings", "onehop_path", "nhop_path"]
    fields = ["nhop_path"]

    json_path = "data/nl2sparql_pairs.json"
    output_path = "experiments/results/output_eval.txt"

    # Load JSON
    if not os.path.exists(json_path):
        print(f"File  not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Find the requested entry
    entry = next((item for item in data if item.get("idx") == idx), None)
    if entry is None:
        print(f"No entry found with idx={idx}")
        return
    
    prompt = make_prompt(entry, fields)

    # exist_ok tells it to keep going and not crash if file already exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print("Prompt written!")

if __name__ == "__main__":
    main()
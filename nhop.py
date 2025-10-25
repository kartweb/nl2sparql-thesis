from methods.multihop import MultiHop
import json

def save_hop_path(idx, path, hop_type="onehop"):
    with open("data/nl2sparql_pairs.json", "r") as f:
        pairs = json.load(f)
    
    if 0 <= idx < len(pairs):
        if hop_type == "nhop":
            pairs[idx]["nhop_path"] = path
            print("N-hop path saved")
        else:
            pairs[idx]["onehop_path"] = path
            print("One-hop path saved")
    else:
        print(f"Index {idx} out of range.")
        return
    
    with open("data/nl2sparql_pairs.json", "w") as f:
        json.dump(pairs, f, indent=2)


if __name__ == "__main__":
    idx = 2
    term = "<https://w3id.org/CMEO/time-chf/angina>"
    
    mh = MultiHop()
    path = mh.retrieve_one_hop(term)
    
    save_hop_path(idx, path)
    print(path)
from methods.multihop import MultiHop
import json

def save_hop_path(idx, path, hop_type="onehop"):
    with open("data/nl2sparql_pairs.json", "r") as f:
        pairs = json.load(f)
    
    if 0 <= idx < len(pairs):
        if hop_type == "nhop":
            if "nhop_path" in pairs[idx]:
                pairs[idx]["nhop_path"].append(path)
            else:
                pairs[idx]["nhop_path"] = [path]
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
    mh = MultiHop()
    idx = 8
    start = "https://w3id.org/CMEO/dp5/observational_design/protocol"
    end = "https://w3id.org/CMEO/dp5/outcome_specification"

    path = mh.retrieve_n_hops(start, end)
    
    save_hop_path(idx, path, hop_type="nhop")
    print(path)

    
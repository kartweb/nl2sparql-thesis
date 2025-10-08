import json

class Getter:
    def __init__(self, dataset_path="data/nl2sparql_pairs.json"):
        self.dataset_path = dataset_path

    def load_data(self):
         with open(self.dataset_path, "r") as f:
            all_pairs = json.load(f)
            return all_pairs

    # get full entry by index
    def get_entry(self, idx):
        data = self.load_data()
        for entry in data:
            if entry.get("idx") == idx:
                return entry
        raise ValueError(f"Entry with idx {idx} not found.")
    
    def get_nl(self, idx):
        return self.get_entry(idx)["nl"]
    
    def get_sparql(self, idx):
        return self.get_entry(idx)["sparql"]
    
    def get_triples(self, idx):
        entry = self.get_entry(idx)
        triples = entry.get("retrieved_triples", {}) # safely handle missing keys
        return triples
    
    def get_fewshot(self, idx):
        entry = self.get_entry(idx)
        fewshot = entry.get("fewshot", {}) # safely handle missing keys
        return fewshot
    
if __name__ == "__main__":
    getter = Getter()
    idx = 4
    out = str(getter.get_triples(idx))
    with open("utils/output.txt", "w",encoding="utf-8") as f:
        f.write(out)


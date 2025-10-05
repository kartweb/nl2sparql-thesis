import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FewShot:
    def __init__(self, current_path="data/current_pair.json", dataset_path="data/nl2sparql_pairs.json"):
        self.current_path = current_path
        self.dataset_path = dataset_path
    
    def load_data(self):
        with open(self.current_path, "r") as f:
            current_pair= json.load(f)
        with open(self.dataset_path, "r") as f:
            all_pairs = json.load(f)
        return current_pair, all_pairs
    
    def find_most_similar(self):
        current_pair, all_pairs = self.load_data()
        current_nl = current_pair["nl"]

        all_nls = [pair["nl"] for pair in all_pairs]

        
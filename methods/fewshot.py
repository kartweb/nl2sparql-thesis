import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FewShot:
    def __init__(self, dataset_path="data/nl2sparql_pairs.json"):
        self.dataset_path = dataset_path
    
    def load_data(self):
        with open(self.dataset_path, "r") as f:
            all_pairs = json.load(f)
        return all_pairs
    
    def find_most_similar(self, current_idx):
        all_pairs = self.load_data()
        current_nl = all_pairs[current_idx]["nl"]

        #Exclude the current pair from the similarity search
        other_nls = [pair["nl"] for i, pair in enumerate(all_pairs) if i != current_idx]

        #fit() learns which words matter and how much
        vectorizer = TfidfVectorizer().fit([current_nl] + other_nls)
        #transform() turns actual text into numeric vectors using that knowledge
        vectors = vectorizer.transform([current_nl] + other_nls)

        #similarities excludes the first vector which is current_nl!
        similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
        best_idx = int(np.argmax(similarities))

        #adjust because we removed one element
        #we map back to all_nls to retain all the data unlike other_nls which only keeps nl part
        adjusted_idx = best_idx if best_idx < current_idx else best_idx + 1
        best_pair = all_pairs[adjusted_idx]
        best_score = similarities[best_idx]
        
        return best_pair, best_score
    
if __name__ == "__main__":
    retriever = FewShot()
    best_pair, best_score = retriever.find_most_similar(1) # example with index 1
    print("Best pair: ", best_pair["nl"])
    print("Best score: ", best_score)
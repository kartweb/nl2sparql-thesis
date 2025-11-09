import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("data/nl2sparql_pairs.json", "r") as f:
    pairs = json.load(f)

cand_pool = [4, 5, 6, 7, 12]
sentences = []
for entry in pairs:
    idx = entry.get("idx", "")
    nl = entry.get("nl", "")
    if idx in cand_pool:
        print(f"Idx({idx}): {nl}.\n")
        sentences.append(nl)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(sentences)

similarity_matrix = cosine_similarity(tfidf_matrix)

print(similarity_matrix)
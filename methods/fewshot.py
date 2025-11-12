import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("data/nl2sparql_pairs.json", "r") as f:
    pairs = json.load(f)

cand_pool = [0,1,2,3,4,5,6,7,8]
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

df = pd.DataFrame(similarity_matrix)
df.to_csv("experiments/results/similarity_matrix.csv")

plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Cosine Similarity Matrix")
plt.tight_layout()
plt.savefig("experiments/results/similarity_matrix_heatmap.png", dpi=300)
plt.close()

# --- Print top 4 most similar for each query ---
print("\nTop 4 most similar sentences per query:")
for i, row in df.iterrows():
    top_sim = row.drop(i).sort_values(ascending=False).head(4)
    top_indices = top_sim.index.tolist()
    print(f"{i}: {', '.join(map(str, top_indices))}")
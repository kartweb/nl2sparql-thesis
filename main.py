import json
from methods.rag import RAG 
from utils.preprocessing import tokenize, remove_stop_words
from utils.embedder import embed_names, embed_sim
import numpy as np
import pandas as pd

def main(current_idx=4):
    rag = RAG() 

    with open("data/nl2sparql_pairs.json", "r") as f:
        pairs = json.load(f) 
    
    for i, p in enumerate(pairs):
        p["idx"] = i

    current_pair = pairs[current_idx]
    tokens = tokenize(current_pair["nl"])
    # remove stop words
    tokens = remove_stop_words(tokens)

    # load precomputed embeddings and correspondings texts
    all_embs = np.load("data/embeddings.npy")
    #stored in text column make the df column into a list
    all_names = pd.read_csv("data/embedding_texts.csv")["text"].tolist()

    retrieved_terms = {}
    retrieved_embeddings = {}

    for token in tokens:
        terms = rag.retrieve_terms(token)
        retrieved_terms[token] = terms

        token_emb = embed_names([token])
        top_matches = embed_sim(token_emb, all_embs, all_names) #should return a numpy array (1, dim)
        retrieved_embeddings[token] = top_matches

    current_pair["retrieved_terms"] = retrieved_terms
    current_pair["retrieved_embeddings"] = retrieved_embeddings

    with open("data/nl2sparql_pairs.json", "w") as f:
        json.dump(pairs, f, indent=2)

    print("done")
   
if __name__ == "__main__":
    main()
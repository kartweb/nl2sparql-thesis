# entry point, runs the pipeline loop

import json
from methods.rag import RAG # class file rag.py
from utils.preprocessing import tokenize # tokenize function from preprocessing.py
from methods.fewshot import FewShot

def main(current_idx=4):
    rag = RAG() 
    fewshot = FewShot()

    # Load all pairs
    with open("data/nl2sparql_pairs.json", "r") as f:
        pairs = json.load(f) 
    
    # Add idx to all pairs if missing
    for i, p in enumerate(pairs):
        p["idx"] = i

    current_pair = pairs[current_idx]
    tokens = tokenize(current_pair["nl"])

    # Retrieve triples
    retrieved = {}
    for token in tokens:
        triples = rag.retrieve_triples(token)
        retrieved[token] = triples

    # Few-shot similarity
    best_pair, best_score = fewshot.find_most_similar(current_idx)

    # Store results
    current_pair["retrieved_triples"] = retrieved
    current_pair["fewshot"] = {
        "similarity_score": best_score,
        "best_match_nl": best_pair["nl"],
        "best_match_sparql": best_pair["sparql"]
    }

    # Write updated data back to same file
    with open("data/nl2sparql_pairs.json", "w") as f:
        json.dump(pairs, f, indent=2)

    print("done")
   
if __name__ == "__main__":
    main()
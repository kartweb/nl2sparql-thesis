# entry point, runs the pipeline loop

import json
from methods.rag import RAG # class file rag.py
from utils.preprocessing import tokenize # tokenize function from preprocessing.py

def main():
    # 1. init Blazegraph connection
    rag = RAG(endpoint_url="http://localhost:9999/blazegraph/sparql") # create RAG instance with Blazegraph SPARQL endpoint

    # 2. load your nl-sparql dataset
    with open("data/current_pair.json", "r") as f:
        pairs = json.load(f) # load dataset from JSON file

    
    # 3. preprocess, tokenize, and json dump results
    retrieved = {}
    for pair in pairs:
        tokens = tokenize(pair["nl"])
        for token in tokens:
            triples = rag.retrieve_triples(token)
            retrieved[token] = triples

    with open("data/retrieved_triples.json", "w") as f:
        json.dump(retrieved, f, indent=2)

if __name__ == "__main__":
    main()
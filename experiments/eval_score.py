import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import re
import os

def normalize_vars(tokens):

    # Make sure they are all lowercase for matching
    prefixes = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "dc": "http://purl.org/dc/elements/1.1/",
        "bfo": "http://purl.obolibrary.org/obo/bfo.owl/",
        "obi": "http://purl.obolibrary.org/obo/obi.owl/",
        "ro": "http://purl.obolibrary.org/obo/ro.owl/",
        "iao": "http://purl.obolibrary.org/obo/iao.owl/",
        "sio": "http://semanticscience.org/ontology/sio.owl/",
        "duo": "http://purl.obolibrary.org/obo/duo/",
        "obcs": "http://purl.obolibrary.org/obo/obcs.owl/",
        "stato": "http://purl.obolibrary.org/obo/stato.owl/",
        "cdi": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
        "cd": "http://citydata.wu.ac.at/ns#",
        "cmeo": "https://w3id.org/cmeo/"
    }



    cleaned_tokens = []
    iri_pattern = re.compile(r"<([^<>]+)>") # matches anything inside <...>
    for t in tokens:

        # Token to lowercasee and remove extra whitespace
        t = t.lower().strip()
        

        # Remove inline comments starting with '#' that are not in uri's <>
        if "#" in t and not re.search(r"<[^>]*#.*?>", t):
            t = t.split("#", 1)[0].strip()
        if not t:
            continue

        # Normalize variables
        if t.startswith("?"):
            cleaned_tokens.append("?var")
            continue

        # Normalize full IRIs to prefixed form
        def replace_iri(match):
            iri = match.group(1) # part inside parentheses
            for prefix, base in prefixes.items():
                if iri.startswith(base):
                    return prefix + ":" + iri[len(base):]
            # if no prefix match return original <...>
            return "<" + iri + ">"
        
        # Replace all <...> occurences in the token
        new_t = iri_pattern.sub(replace_iri, t)
        cleaned_tokens.append(new_t)

    return cleaned_tokens

def bleu(reference, candidate):

    if not isinstance(reference, str):
        reference = ""
    if not isinstance(candidate, str):
        candidate = ""

    ref_tokens = reference.split()
    cand_tokens = candidate.split()

    # Normalize SPARQL variable names
    ref_tokens = normalize_vars(ref_tokens)
    cand_tokens = normalize_vars(cand_tokens)

    #Use smoothing function to avoid zero scores for short sequences, adding 1 to numerator and denominator to all n
    smoothie = SmoothingFunction().method1
    #Wrap references in list because BLEU allows multiple references
    return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie) 

def run_eval(input_excel, cols, output_prefix):
    df = pd.read_excel(input_excel)
    
    # === Build a new DataFrame just for normalized text ===
    df_clean = pd.DataFrame()
    df_clean["query_id"] = df["query_id"]

    # Apply normalization to each relevant column
    for col in ["gold_standard"] + cols:
        if col in df.columns:
            df_clean[col + "_cleaned"] = df[col].apply(lambda x: " ".join(normalize_vars(str(x).split())))

    # Save only cleaned data for inspection
    df_clean.to_csv(f"experiments/results/{output_prefix}_output.csv", index=False)
    
    # Compute BLEU for each provided column
    for col in cols:
        if col in df.columns:
            df[f"bleu_{col}"] = df.apply(lambda row: bleu(row["gold_standard"], row[col]), axis=1)

    keep_cols = ["query_id"] + [f"bleu_{c}" for c in cols]
    df = df[[c for c in keep_cols if c in df.columns]]

    avg_row = df.mean(numeric_only=True)
    avg_row["query_id"] = "Average"
    df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)
    
    print(df)
    df.to_csv(f"experiments/results/{output_prefix}_score.csv", index=False)
    print("done")

if __name__ == "__main__":
    # Methods Eval
    run_eval(
        input_excel="experiments/results/methods_eval.xlsx",
        cols=[
            "with_terms",
            "with_embeddings",
            "with_nhop"
        ],
        output_prefix="methods_eval"
    )

    # Fewshot Eval
    run_eval(
        input_excel="experiments/results/fewshot_eval.xlsx",
        cols = [
            "0shot",
            "1shot",
            "2shot",
            "3shot",
            "4shot"
        ],
        output_prefix="fewshot_eval"
    )

    # Schema Eval
    run_eval(
        input_excel="experiments/results/schema_eval.xlsx",
        cols=[
            "no_schema",
            "schema_p",
            "schema_p_filtered",
            "schema_po_filtered",
            "schema_poi_filtered",
            "schema_poi_filtered_improved_prompt"
        ],
        output_prefix="schema_eval"
    )

    # LLM eval
    run_eval(
        input_excel="experiments/results/llm_eval.xlsx",
        cols = [
            "GPT-5_instant",
            "Mistral_7B"
        ],
        output_prefix="llm_eval"
    )

    print("\n✅ All evaluations completed successfully!")
    
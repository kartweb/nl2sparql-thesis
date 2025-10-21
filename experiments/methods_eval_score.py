import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import re

def normalize_vars(tokens):

    # Make sure they are all lowercase for matching
    prefixes = {
        "bfo": "http://purl.obolibrary.org/obo/bfo.owl/",
        "cdio": "https://w3id.org/cdio/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "ns1": "http://purl.obolibrary.org/obo/bfo.owl#",
        "obi": "http://purl.obolibrary.org/obo/obi.owl/",
        "xsd": "http://www.w3.org/2001/xmlschema#"
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

# Bleu scores measure precision foucusing on how much generated text
# matches the reference text in terms of word order and structure
# making it good for machine translation
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

if __name__ == "__main__":
    df = pd.read_excel(r"experiments/results/methods_eval.xlsx")
    
    # === Build a new DataFrame just for normalized text ===
    df_clean = pd.DataFrame()
    df_clean["query_id"] = df["query_id"]

    # Apply normalization to each relevant column
    for col in ["gold_standard", "with_terms", "with_embeddings", "with_onehop", "with_nhop", "with_nhop_terms_embs"]:
        if col in df.columns:
            df_clean[col + "_cleaned"] = df[col].apply(lambda x: " ".join(normalize_vars(str(x).split())))

    # Save only cleaned data for inspection
    df_clean.to_csv("experiments/results/methods_eval_output.csv", index=False)
    
    
    # Pandas apply method is the one that iterates through each row therefore we use the lambda function
    df["bleu_terms"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_terms']), axis=1)
    df["bleu_embs"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_embeddings']), axis=1)
    df["bleu_onehop"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_onehop']), axis=1)
    df["bleu_nhop"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_nhop']), axis=1)
    df["bleu_nhop_terms_embs"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_nhop_terms_embs']), axis=1)


    keep_cols = ["query_id", "bleu_terms", "bleu_embs", "bleu_onehop", "bleu_nhop", "bleu_nhop_terms_embs"]
    df = df[[c for c in keep_cols if c in df.columns]]

    avg_row = df.mean(numeric_only=True) #computes average of each numeric column and returns series
    avg_row["query_id"] = "Average" # add one extra label to series
    #Forget old row indexes from both dataframes and give a new clean continuous 0-based index
    df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True) # Add series row 0 by default using concat 

    print(df)

    df.to_csv("experiments/results/methods_eval_score.csv", index=False)

    print('done')
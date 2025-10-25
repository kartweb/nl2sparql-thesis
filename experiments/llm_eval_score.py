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

def bleu(reference, candidate):
    if not isinstance(reference, str):
        reference = ""
    if not isinstance(candidate, str):
        candidate = ""

    ref_tokens = normalize_vars(reference.split())
    cand_tokens = normalize_vars(candidate.split())

    smoothie = SmoothingFunction().method1
    return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie)

model_cols = [
    "GPT-5_instant",
    "GPT-4o",
    "Deepseek",
    "Gemini_2.5-Flash",
    "Claude_Sonnet-4.5",
    "Mistral_7B",
]

if __name__ == "__main__":
    df = pd.read_excel("experiments/results/llm_eval.xlsx")

     # === Build a new DataFrame just for normalized text ===
    df_clean = pd.DataFrame()
    df_clean["query_id"] = df["query_id"]

    # Normalize gold standard and all model outputs
    for col in ["gold_standard"] + model_cols:
        if col in df.columns:
            df_clean[col + "_cleaned"] = df[col].apply(lambda x: " ".join(normalize_vars(str(x).split())))

    # Save cleaned data to inspect normalization
    df_clean.to_csv("experiments/results/llm_eval_output.csv", index=False)

    for model in model_cols:
        if model in df.columns:
            bleu_col = f"bleu_{model}"
            df[bleu_col] = df.apply(lambda row: bleu(row["gold_standard"], row[model]), axis=1)

    # Keep only relevant columns
    keep_cols = ["query_id"] + [c for c in df.columns if c.startswith("bleu_")]
    df = df[[c for c in keep_cols if c in df.columns]]

    avg_row = df.mean(numeric_only=True)
    avg_row["query_id"] = "Average" 
    df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    df["average"] = df.mean(axis=1, numeric_only=True)

    print(df)
    df.to_csv("experiments/results/llm_eval_score.csv", index=False)
    print("done")
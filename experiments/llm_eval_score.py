import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def normalize_vars(tokens):

    prefixes = {
        "bfo": "http://purl.obolibrary.org/obo/bfo.owl/",
        "cdio": "https://w3id.org/CDIO/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "ns1": "http://purl.obolibrary.org/obo/bfo.owl#",
        "obi": "http://purl.obolibrary.org/obo/obi.owl/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    }

    cleaned_tokens = []
    for t in tokens:
        # Token to lowercasee and remove extra whitespace
        t = t.lower().strip()

        # Remove inline comments starting with '#'
        if "#" in t:
            t = t.split("#", 1)[0].strip()
        if not t:
            continue

        # Normalize variables
        if t.startswith("?"):
            cleaned_tokens.append("?var")
            continue

        # Normalize full IRIs to prefixed form
        if t.startswith("<") and t.endswith(">"):
            iri = t[1:-1]
            replaced = False
            for prefix, base in prefixes.items():
                if iri.startswith(base):
                    short_form = prefix + ":" + iri[len(base):]
                    cleaned_tokens.append(short_form)
                    replaced = True
                    break
            if not replaced:
                cleaned_tokens.append(t)
        else:
            cleaned_tokens.append(t)

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
    "MetaAI_Llama-4",
    "Gemini_2.5-Flash",
    "Claude_Sonnet-4.5",
    "Mistral_7B",
    "GPT-5_thinking",
    "Deepseek",
    "Deepseek_DeepThink"
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

    print(df)
    df.to_csv("experiments/results/llm_eval_score.csv", index=False)
    print("done")
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

df = pd.read_excel("experiments/results/terms_vs_embs.xlsx")

# Replace all tokens starting with '?' with a generic placeholder
def normalize_vars(tokens):
    return ["?var" if t.startswith("?") else t for t in tokens]

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
    
# Pandas apply method is the one that iterates through each row therefore we use the lambda function
df["bleu_terms"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_terms']), axis=1)
df["bleu_embs"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_embeddings']), axis=1)
df["bleu_onehop"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_onehop']), axis=1)
df["bleu_nhop"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_nhop']), axis=1)
df["bleu_nhop_terms_embs"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_nhop_terms_embs']), axis=1)

keep_cols = ["query_id", "bleu_terms", "bleu_embs", "bleu_onehop", "bleu_nhop", "bleu_nhop_terms_embs"]

df = df[[c for c in keep_cols if c in df.columns]]

print(df)

df.to_csv("experiments/results/terms_vs_embs_eval.csv", index=False)

print('done')
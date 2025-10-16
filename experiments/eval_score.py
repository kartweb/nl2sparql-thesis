import pandas as pd
from difflib import SequenceMatcher

df = pd.read_excel("experiments/results/terms_vs_embs.xlsx")

def fuzz_positive_overlap(reference, candidate, threshold=0.8):
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    matches = 0
    for ref in ref_tokens:
        for cand in cand_tokens:
            if SequenceMatcher(None, ref, cand).ratio() >= threshold:
                matches += 1
                break
    return matches / len(ref_tokens) if ref_tokens else 0


# Fuzzy recall (reward only good partial matches)
# Pandas apply method is the one that iterates through each row therefore we use the lambda function
df["fuzzy_recall_terms"] = df.apply(lambda row: fuzz_positive_overlap(row['gold_standard'], row['with_terms']), axis=1)
df["fuzzy_recall_embs"] = df.apply(lambda row: fuzz_positive_overlap(row['gold_standard'], row['with_embeddings']), axis=1)

keep_cols = ["query_id", "fuzzy_recall_terms", "fuzzy_recall_embs"]

df = df[[c for c in keep_cols if c in df.columns]]

print(df)

df.to_csv("experiments/results/terms_vs_embs_eval.csv", index=False)

print('done')
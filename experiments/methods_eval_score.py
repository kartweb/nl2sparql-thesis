import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

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
            # python list slicing , first one is included: last one excluded
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
    # Pandas apply method is the one that iterates through each row therefore we use the lambda function
    df["bleu_terms"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_terms']), axis=1)
    df["bleu_embs"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_embeddings']), axis=1)
    df["bleu_onehop"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_onehop']), axis=1)
    df["bleu_nhop"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_nhop']), axis=1)
    df["bleu_nhop_terms_embs"] = df.apply(lambda row: bleu(row['gold_standard'], row['with_nhop_terms_embs']), axis=1)


    keep_cols = ["query_id", "bleu_terms", "bleu_embs", "bleu_onehop", "bleu_nhop", "bleu_nhop_terms_embs"]

    df = df[[c for c in keep_cols if c in df.columns]]

    print(df)

    df.to_csv("experiments/results/methods_eval_score.csv", index=False)

    print('done')
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

df = pd.read_csv("results/terms_vs_embs.csv")

df["blue_terms"] = df.apply()
#Helper function to embed a NL question

import numpy as np
import torch
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

def embed_names(all_names, batch_size=128):
    
    tokenizer = AutoTokenizer.from_pretrained("cambridgeltl/SapBERT-from-PubMedBERT-fulltext")
    model = AutoModel.from_pretrained("cambridgeltl/SapBERT-from-PubMedBERT-fulltext").cuda()
    model.eval()

    all_embs = []
    for i in tqdm(np.arange(0, len(all_names), batch_size)):
        toks = tokenizer.batch_encode_plus(
            all_names[i:i+batch_size],
            padding="max_length",
            max_length=25,
            truncation=True,
            return_tensors="pt"
        )
        toks_cuda = {k: v.cuda() for k, v in toks.items()}
        with torch.no_grad():
            cls_rep = model(**toks_cuda)[0][:, 0, :]  # CLS token
        all_embs.append(cls_rep.cpu().numpy())

    all_embs = np.concatenate(all_embs, axis=0)
    return all_embs

def embed_sim(token_emb, all_embs, all_names):
    sims = cosine_similarity(token_emb, all_embs)[0] # [0] cus im only passing one word
    top_idx = np.argsort(sims)[::-1][:30] # Sort descending top 5 most similar

    top_matches = [
        {"text": all_names[j], "score": float(sims[j])}
        for j in top_idx
    ]
    return top_matches




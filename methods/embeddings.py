import numpy as np
import pandas as pd
import torch
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModel  

tokenizer = AutoTokenizer.from_pretrained("cambridgeltl/SapBERT-from-PubMedBERT-fulltext")  
model = AutoModel.from_pretrained("cambridgeltl/SapBERT-from-PubMedBERT-fulltext").cuda()

df = pd.read_csv("data/studiesAllTriples.csv")

# Stack columns row by row then make them into a list essentially splitting them individually
all_names = pd.concat([df["s"], df["p"], df["o"]], axis=0).astype(str).tolist()

# Batch embedding to avoid GPU overflow
bs = 128 
all_embs = []
for i in tqdm(np.arange(0, len(all_names), bs)):
    toks = tokenizer.batch_encode_plus(
        all_names[i:i+bs],
        padding="max_length",
        max_length=25,
        truncation=True,
        return_tensors="pt"
    )
    toks_cuda = {k: v.cuda() for k, v in toks.items()}
    cls_rep = model(**toks_cuda)[0][:, 0, :]  # CLS token representation
    all_embs.append(cls_rep.cpu().detach().numpy())

# Combine all batches
all_embs = np.concatenate(all_embs, axis=0)

# Save embeddings to disk
np.save("data/embeddings.npy", all_embs)

# Save corresponding text for retrieval
pd.DataFrame({"text": all_names}).to_csv("data/embedding_texts.csv", index=False)
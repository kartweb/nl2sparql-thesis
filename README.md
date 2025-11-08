# NL2SPARQL-THESIS

**NL2SPARQL-THESIS** is a research project exploring methods to translate **natural language questions** into **SPARQL queries** for knowledge graph querying.  
It implements and compares different strategies — including **Retrieval-Augmented Generation (RAG)**, **Few-Shot Learning**, and **Schema Feeding** — to understand how language models reason about structured data and logical queries.

---

## ⚙️ Installation Requirements
  
To install dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

Below are the main scripts you can run for different components of the project.

### Text match and Embeddings pipeline

Replace `current_idx` in `main(current_idx=13)` with the index (`idx`) of the pair you want from `data/nl2sparql_pairs.json`. Then run main()

### Nhop pipeline


This script performs **multi-hop (or one-hop)** relation retrieval starting from a given ontology term.

**Steps:**
1. Set the `idx` — the index of the example from `data/nl2sparql_pairs.json`.
2. Set the `term` — the ontology term to start the hop chaining from.
3. Choose the retrieval method:
   - `mh.retrieve_one_hop(term)` for one-hop relations
   - `mh.retrieve_n_hops(term)` for n-hop relations
4. The retrieved path is automatically saved back into the same JSON file via `save_hop_path()`:
   - `hop_type="onehop"` (default)  
   - `hop_type="nhop"` for multi-hop chains

## Ethics statement

Clinical data were provided by the Institute of Data Science (IDS), Maastricht University, under the Code of Conduct for Reuse of Clinical Data for Research Purposes. IDS data are pseudonymized and handled in compliance with applicable privacy regulations.


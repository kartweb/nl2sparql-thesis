# Retrieval-Augmented Generation and Few-Shot Learning for Natural Language to SPARQL in a Heart Failure Metadata Knowledge Graph

This is a research project exploring methods to translate **natural language questions** into **SPARQL queries** for knowledge graph querying.  
It implements and compares different strategies including **Retrieval-Augmented Generation (RAG)** and **Few-Shot Learning** to understand how different language models reason about structured data and logical queries.

---
## Data
The raw Nl to SPARQL pairs are in:
`data/nl2sparql_pairs.txt`

## Installation Requirements
  
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

### prompt_generator

Generates a **text prompt** for SPARQL generation using a selected entry from `data/nl2sparql_pairs.json`.

You can specify:
- `idx` → which entry to use (matches the `idx` in the dataset)  
- `fields` → which optional fields to include in the prompt  
  (choose from `retrieved_terms`, `retrieved_embeddings`, `onehop_path`, or `nhop_path`)

The generated prompt is saved to:
experiments/results/generated_prompt.txt

See the improved and revised prompt template containing
two templates (zero-shot and few-shot) ready to use in:
data/revised_prompt_nl_sparql.pdf
### Eval Score

Evaluates generated SPARQL queries using **BLEU scores** across multiple experiment files.

This script automatically normalizes SPARQL variables and IRIs, computes BLEU scores for each experiment column, and saves both cleaned text and score results.

You can also modify the given cols list for the experiments or add totally new experiments into main for evaluation.


### Utils

This folder contains small helper scripts for working with the `data/nl2sparql_pairs.json` dataset.

---

#### Clean Data (`clean_pairs.py`)
Cleans the dataset by **keeping only selected fields** and removing the rest.

Default fields kept:
- `nl`
- `nl_keywords`
- `sparql`
- `graph`
- `prefix`

You can modify the list inside the script to control which fields are preserved:
```python
{k: item[k] for k in ("nl", "nl_keywords", "sparql", "graph", "prefix") if k in item}
```

#### Getter

A lightweight utility for **retrieving entries or specific fields** from `data/nl2sparql_pairs.json`.

**Functions:**
- `get_entry(idx)` → returns the full entry with the given index  
- `get_nl(idx)` → returns the natural language question  
- `get_sparql(idx)` → returns the corresponding SPARQL query  
- `get_terms(idx)` → returns retrieved terms (if available)  
- `get_embeddings(idx)` → returns retrieved embeddings (if available)




## Ethics statement

Clinical data were provided by the Institute of Data Science (IDS), Maastricht University, under the Code of Conduct for Reuse of Clinical Data for Research Purposes. IDS data are pseudonymized and handled in compliance with applicable privacy regulations.

## CMEO ontology 
The CMEO ontology used to construct the metadata knowledge graphs is available at: https://github.com/komi786/cmeo/tree/v1.0.1
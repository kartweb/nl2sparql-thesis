# NL2SPARQL-THESIS

**NL2SPARQL-THESIS** is a research project exploring methods to translate **natural language questions** into **SPARQL queries** for knowledge graph querying.  
It implements and compares different strategies — including **Retrieval-Augmented Generation (RAG)**, **Few-Shot Learning**, and **Schema Feeding** — to understand how language models reason about structured data and logical queries.

---

## ⚙️ Installation Requirements

Before running the project, make sure you have **Python 3.10+** installed.  
To install dependencies, run:

```bash
pip install -r requirements.txt
If you want to use a virtual environment (recommended), set it up before installing:

bash
Copy code
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
📁 Directory Overview
graphql
Copy code
NL2SPARQL-THESIS/
│
├── data/                        # Datasets, schema files, and sample inputs
│
├── experiments/
│   ├── results/                 # Stores experiment results and evaluation outputs
│   │   └── eval_score.py        # Script to compute evaluation metrics (accuracy, BLEU, etc.)
│   │
│   ├── prompt_generator.py      # Builds prompts dynamically for LLM-based SPARQL generation
│   │
│   └── methods/                 # Core experimental methods and algorithms
│       ├── embeddings.py        # Embedding utilities for retrieval and similarity search
│       ├── fewshot.py           # Few-shot prompting and inference experiments
│       ├── multihop.py          # Multi-hop reasoning experiments
│       ├── rag.py               # Retrieval-Augmented Generation pipeline
│       └── schema_feeding.py    # Schema-aware SPARQL generation approach
│
├── unit-tests/                  # Unit test scripts for validation
│   ├── unit-test_norm           # Normalization and text preprocessing tests
│   └── unit-test_rag            # Tests for the RAG pipeline
│
├── utils/                       # Utility functions shared across modules
│   ├── clear_dict.py            # Helper script for cleaning JSON/dictionary outputs
│   ├── embedder/                # Embedding model utilities
│   ├── getter.py                # Data fetching and retrieval helpers
│   ├── preprocessing.py         # Text preprocessing (tokenization, cleaning)
│   └── output.txt               # Temporary or debug output file
│
├── nhop.py                      # Multi-hop question reasoning and evaluation
├── main.py                      # Entry point for running experiments
├── requirements.txt             # Python dependencies
└── .gitignore                   # Git ignore rules
# Financial Crime Investigation AI Agent

A modular educational project using Python, SQLite, LangGraph, optional Groq LLM explanations, and retrieval of compliance policy documents.

## Important design boundaries
- Transaction detection is deterministic Python code. The LLM does not calculate totals or decide whether a transaction is suspicious.
- An alert is an indicator for review, not proof of money laundering or other wrongdoing.
- The system produces decision-support material only. A qualified human analyst makes any escalation or filing decision.
- The sample records and customer profiles are synthetic. Do not use real personal or banking data in this demo.

## Input transaction schema

The transaction CSV follows the supplied format:

`txn_id,account_id,counterparty,amount,direction,timestamp,channel`

`customer_id` is not required. Investigations are keyed by `account_id`.

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add a Groq API key to `.env` to enable LLM-generated narrative. Without a key, the project creates a deterministic report.

## Configure data
- Replace `data/transactions.csv` with your dataset, keeping the exact column names.
- Add or edit optional account profiles in `data/account_profiles.csv`.
- Add policy PDFs or TXT files under `data/policies/`.

## Initialize SQLite

```powershell
python -m database.seed_data
```

## Build / refresh the policy retrieval index

```powershell
python -m rag.build_index
```

The starter retriever uses TF-IDF text vectors so it can run locally without downloading embedding models. It can later be replaced with sentence-transformer embeddings and a vector database.

## Run one account investigation

```powershell
python main.py --account-id ACC-3010
```

## Run the API

```powershell
uvicorn api.routes:app --reload
```

Open `http://127.0.0.1:8000/docs`. POST `/investigate` with:

```json
{"account_id": "ACC-3010"}
```

## Tests

```powershell
pytest -q
```

## Workflow

1. Read transactions for the requested account from SQLite.
2. Run deterministic credit-structuring detection on the supplied transaction schema.
3. Retrieve optional account profile and historical alerts.
4. Retrieve relevant policy snippets.
5. Pass structured evidence into a LangGraph workflow.
6. Optionally ask Groq to write a cautious analyst-facing explanation.
7. Return and save a report with evidence and a human-review recommendation.

## Notes about the starter detection rule

The included rule flags groups of at least `min_transaction_count` credit transactions where:
- each transaction is individually below the configured threshold,
- transactions belong to the same account,
- their combined amount is greater than the threshold, and
- they fall within the configured rolling time window.

This is a configurable educational example, not a complete AML monitoring system. Tune thresholds only against approved policy and labelled validation data.

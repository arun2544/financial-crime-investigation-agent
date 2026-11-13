# Financial Crime Investigation AI Agent

An AI-powered financial crime investigation system built using **Python, LangGraph, FastAPI, SQLite, RAG, and Groq LLM** to identify potentially suspicious banking transactions and generate evidence-based investigation reports.

## Key Features

- Deterministic transaction pattern detection (structuring).
- AI agent workflow orchestration using LangGraph.
- Account, transaction, and historical alert retrieval.
- RAG-based AML policy retrieval using TF-IDF.
- Optional Groq LLM for analyst-friendly explanations.
- FastAPI backend with REST endpoints.
- Interactive frontend dashboard using HTML, CSS, and JavaScript.

## Architecture

```text
Transaction Data
       |
       v
  SQLite Database
       |
       v
  Python Tools
       |
       v
Deterministic Detection
       |
       v
 LangGraph Workflow
       |
    +--+--+
    |     |
    v     v
   RAG   Evidence
    |     |
    +--+--+
       |
       v
   Groq LLM
   (Optional)
       |
       v
Investigation Report
       |
       v
 FastAPI + Frontend
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python, Pandas | Data processing |
| SQLite | Database |
| LangGraph | Agent orchestration |
| Groq LLM | AI explanations |
| RAG, TF-IDF | Policy retrieval |
| FastAPI | Backend API |
| HTML, CSS, JavaScript | Frontend |
| Pytest | Testing |

## Project Structure

```text
financial-crime-investigation-agent/
├── agent/
├── api/
├── config/
├── data/
├── database/
├── detector/
├── evaluation/
├── frontend/
├── llm/
├── rag/
├── tests/
├── tools/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/arun2544/financial-crime-investigation-agent.git
cd financial-crime-investigation-agent
```

**2. Create and activate virtual environment**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment**

```powershell
Copy-Item .env.example .env
```

Add your Groq API key to `.env` (optional).

**5. Initialize database and RAG index**

```bash
python -m database.seed_data
python -m rag.build_index
```

## Run the Application

**Backend:**

```bash
uvicorn api.routes:app --reload
```

API documentation: http://127.0.0.1:8000/docs

**Frontend (in a second terminal):**

```bash
cd frontend
python -m http.server 5500
```

Dashboard: http://127.0.0.1:5500

**CLI investigation:**

```bash
python main.py --account-id ACC-3010
```

## Testing

```bash
python -m pytest -q
```

## Detection Logic

The system identifies potential structuring patterns where:

- Multiple credit transactions belong to the same account.
- Each transaction is below the configured threshold.
- Their combined amount exceeds the threshold.
- Transactions occur within the configured rolling time window.

## Important Design Decisions

- Transaction detection uses deterministic Python rules.
- The LLM only explains structured evidence; it does not decide whether transactions are suspicious.
- RAG provides relevant AML policy context.
- Investigation reports support human review, not automated compliance decisions.

## Disclaimer

This is an educational project using synthetic banking data. It is not a production AML monitoring system. All investigation findings require qualified human review.

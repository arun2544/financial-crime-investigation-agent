
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    InvestigationRequest,
    InvestigationResponse,
)
from agent.agent_runner import run_investigation

app = FastAPI(
    title="Sentinel Financial Crime Investigation API",
    description=(
        "AI-powered financial crime investigation "
        "using deterministic detection, RAG and LLM explanations."
    ),
    version="1.0.0",
)

# Allow requests from the local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def root():
    return {
        "message": "Sentinel Financial Crime Investigation API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "financial-crime-investigation-agent",
    }


@app.post(
    "/investigate",
    response_model=InvestigationResponse,
)
def investigate(request: InvestigationRequest):

    try:
        result = run_investigation(request.account_id)

        return InvestigationResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {str(exc)}",
        )

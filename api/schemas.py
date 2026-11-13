
from typing import Any
from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    account_id: str = Field(
        ...,
        min_length=1,
        description="Bank account ID to investigate",
        examples=["ACC-3010"],
    )


class InvestigationResponse(BaseModel):
    account_id: str
    transactions_reviewed: int

    account_profile: dict[str, Any] = Field(
        default_factory=dict
    )

    transaction_evidence: list[dict[str, Any]] = Field(
        default_factory=list
    )

    previous_alerts: list[dict[str, Any]] = Field(
        default_factory=list
    )

    policy_context: list[dict[str, Any]] = Field(
        default_factory=list
    )

    findings: str
    recommendation: str
    disclaimer: str

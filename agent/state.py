from typing import TypedDict

class InvestigationState(TypedDict, total=False):
    account_id: str
    transactions: list[dict]
    account_profile: dict | None
    previous_alerts: list[dict]
    transaction_evidence: list[dict]
    policy_context: list[dict]
    findings: str
    recommendation: str
    final_report: dict

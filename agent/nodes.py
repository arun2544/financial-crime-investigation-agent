import pandas as pd
from agent.state import InvestigationState
from database.db import CONFIG
from tools.transaction_tool import get_account_transactions
from tools.customer_tool import get_account_profile
from tools.alert_tool import get_previous_alerts
from tools.policy_tool import get_policy_context
from detector.structuring import detect_structuring
from llm.llm_client import explain_investigation

def gather_evidence(state: InvestigationState) -> InvestigationState:
    account_id = state["account_id"]
    txns = get_account_transactions(account_id)
    profile = get_account_profile(account_id)
    alerts = get_previous_alerts(account_id)
    rule_cfg = CONFIG["structuring"]
    evidence = detect_structuring(
        pd.DataFrame(txns),
        threshold=rule_cfg["threshold"],
        rolling_window_hours=rule_cfg["rolling_window_hours"],
        min_transaction_count=rule_cfg["min_transaction_count"],
    ) if txns else []
    policy = get_policy_context(
        "transaction monitoring credit structuring account activity analyst review",
        top_k=4,
    )
    return {
        **state,
        "transactions": txns,
        "account_profile": profile,
        "previous_alerts": alerts,
        "transaction_evidence": evidence,
        "policy_context": policy,
    }

def create_report(state: InvestigationState) -> InvestigationState:
    evidence_bundle = {
        "account_id": state["account_id"],
        "transaction_evidence": state.get("transaction_evidence", []),
        "account_profile": state.get("account_profile"),
        "previous_alerts": state.get("previous_alerts", []),
        "policy_context": state.get("policy_context", []),
    }
    llm_text = explain_investigation(evidence_bundle)
    patterns = state.get("transaction_evidence", [])
    if llm_text:
        findings = llm_text
    elif patterns:
        findings = (
            f"The configured monitoring rule matched {len(patterns)} transaction pattern(s). "
            "This is an alert indicator and requires contextual review; it is not proof of wrongdoing."
        )
    else:
        findings = "No transaction patterns matched the configured structuring rule in the available data."

    recommendation = (
        "Refer the alert and supporting evidence to a qualified human compliance analyst."
        if patterns or state.get("previous_alerts")
        else "No escalation is indicated by this rule alone. Continue monitoring under approved procedures."
    )
    report = {
        "account_id": state["account_id"],
        "transactions_reviewed": len(state.get("transactions", [])),
        "account_profile": state.get("account_profile"),
        "transaction_evidence": patterns,
        "previous_alerts": state.get("previous_alerts", []),
        "policy_context": state.get("policy_context", []),
        "findings": findings,
        "recommendation": recommendation,
        "disclaimer": "Decision-support output only. A human analyst must review before any action."
    }
    return {**state, "findings": findings, "recommendation": recommendation, "final_report": report}

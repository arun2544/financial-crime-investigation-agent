
from agent.graph import build_graph


def run_investigation(account_id: str):
    """
    Starts the financial crime investigation workflow.
    """

    graph = build_graph()

    initial_state = {
        "account_id": account_id,
        "transactions": [],
        "account_profile": {},
        "transaction_evidence": [],
        "previous_alerts": [],
        "policy_context": [],
        "findings": "",
        "recommendation": "",
        "disclaimer": "",
    }

    result = graph.invoke(initial_state)

    return {
        "account_id": result["account_id"],
        "transactions_reviewed": len(
            result.get("transactions", [])
        ),
        "account_profile": result.get(
            "account_profile", {}
        ),
        "transaction_evidence": result.get(
            "transaction_evidence", []
        ),
        "previous_alerts": result.get(
            "previous_alerts", []
        ),
        "policy_context": result.get(
            "policy_context", []
        ),
        "findings": result.get("findings", ""),
        "recommendation": result.get(
            "recommendation", ""
        ),
        "disclaimer": result.get(
            "disclaimer", ""
        ),
    }

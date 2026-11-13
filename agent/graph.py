from langgraph.graph import StateGraph, START, END
from agent.state import InvestigationState
from agent.nodes import gather_evidence, create_report

def build_graph():
    workflow = StateGraph(InvestigationState)
    workflow.add_node("gather_evidence", gather_evidence)
    workflow.add_node("create_report", create_report)
    workflow.add_edge(START, "gather_evidence")
    workflow.add_edge("gather_evidence", "create_report")
    workflow.add_edge("create_report", END)
    return workflow.compile()

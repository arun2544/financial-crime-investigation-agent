def test_agent_graph_builds():
    from agent.graph import build_graph
    graph = build_graph()
    assert graph is not None

def test_account_tool_functions_import():
    from tools.transaction_tool import get_account_transactions
    from tools.customer_tool import get_account_profile
    from tools.alert_tool import get_previous_alerts
    assert callable(get_account_transactions)
    assert callable(get_account_profile)
    assert callable(get_previous_alerts)

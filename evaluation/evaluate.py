import json
from pathlib import Path
from agent.agent_runner import run_investigation

def main():
    cases = json.loads(Path("evaluation/test_cases.json").read_text(encoding="utf-8"))
    for case in cases:
        report = run_investigation(case["account_id"])
        actual = bool(report["transaction_evidence"])
        print({
            "account_id": case["account_id"],
            "expected": case["expected_rule_alert"],
            "actual": actual,
            "match": actual == case["expected_rule_alert"]
        })

if __name__ == "__main__":
    main()

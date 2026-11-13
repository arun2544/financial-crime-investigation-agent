import argparse
import json
from pathlib import Path
from database.db import initialize_database
from database.seed_data import main as seed_data
from agent.agent_runner import run_investigation

def main():
    parser = argparse.ArgumentParser(description="Financial Crime Investigation Agent")
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--seed", action="store_true", help="Reload SQLite from CSV files")
    args = parser.parse_args()
    initialize_database()
    if args.seed:
        seed_data()
    report = run_investigation(args.account_id)
    output_dir = Path("output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.account_id}_report.json"
    output_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    print(f"\nSaved report: {output_path}")

if __name__ == "__main__":
    main()

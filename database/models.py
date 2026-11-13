from dataclasses import dataclass

@dataclass
class Transaction:
    txn_id: str
    account_id: str
    counterparty: str
    amount: float
    direction: str
    timestamp: str
    channel: str

# models.py
# Data models for the Budget Tracker application
# University Project - Budget Tracker

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Transaction:
    """Represents a single income or expense transaction."""
    title: str
    amount: float
    category: str
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    transaction_type: str = "expense"  # "income" or "expense"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount must be a positive number.")
        if self.transaction_type not in ("income", "expense"):
            raise ValueError("transaction_type must be 'income' or 'expense'.")


@dataclass
class Budget:
    """Holds all transactions and computes budget summary."""
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the budget."""
        self.transactions.append(transaction)

    def get_total_income(self) -> float:
        """Sum of all income transactions."""
        return sum(t.amount for t in self.transactions if t.transaction_type == "income")

    def get_total_expenses(self) -> float:
        """Sum of all expense transactions."""
        return sum(t.amount for t in self.transactions if t.transaction_type == "expense")

    def get_balance(self) -> float:
        """Remaining budget: income minus expenses."""
        return self.get_total_income() - self.get_total_expenses()

    def get_income_transactions(self) -> List[Transaction]:
        return [t for t in self.transactions if t.transaction_type == "income"]

    def get_expense_transactions(self) -> List[Transaction]:
        return [t for t in self.transactions if t.transaction_type == "expense"]

    def clear(self):
        """Remove all transactions."""
        self.transactions.clear()

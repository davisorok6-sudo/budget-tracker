# budget_manager.py
# Business logic / controller layer for the Budget Tracker application
# University Project - Budget Tracker

from models import Budget, Transaction


class BudgetManager:
    """
    Handles all business logic for the budget tracker.
    Acts as the bridge between the GUI and the data models.
    """

    def __init__(self):
        self.budget = Budget()

    # ------------------------------------------------------------------
    # Adding transactions
    # ------------------------------------------------------------------

    def add_income(self, title: str, amount: str, category: str) -> str:
        """
        Validate and add an income entry.
        Returns a success message or raises ValueError on bad input.
        """
        title, amount = self._validate(title, amount)
        transaction = Transaction(
            title=title,
            amount=amount,
            category=category,
            transaction_type="income"
        )
        self.budget.add_transaction(transaction)
        return f"Income '{title}' of ₦{amount:,.2f} added successfully."

    def add_expense(self, title: str, amount: str, category: str) -> str:
        """
        Validate and add an expense entry.
        Returns a success message or raises ValueError on bad input.
        """
        title, amount = self._validate(title, amount)
        transaction = Transaction(
            title=title,
            amount=amount,
            category=category,
            transaction_type="expense"
        )
        self.budget.add_transaction(transaction)
        return f"Expense '{title}' of ₦{amount:,.2f} added successfully."

    # ------------------------------------------------------------------
    # Summary getters
    # ------------------------------------------------------------------

    def get_summary(self) -> dict:
        """Return a dict with income, expenses, and balance totals."""
        return {
            "income": self.budget.get_total_income(),
            "expenses": self.budget.get_total_expenses(),
            "balance": self.budget.get_balance(),
        }

    def get_all_income(self):
        """Return list of income Transaction objects."""
        return self.budget.get_income_transactions()

    def get_all_expenses(self):
        """Return list of expense Transaction objects."""
        return self.budget.get_expense_transactions()

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self):
        """Clear all budget data."""
        self.budget.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate(self, title: str, amount: str):
        """Validate title and amount inputs. Returns (title, float_amount)."""
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        try:
            amount_float = float(amount.strip())
        except ValueError:
            raise ValueError("Amount must be a valid number.")
        if amount_float <= 0:
            raise ValueError("Amount must be greater than zero.")
        return title, amount_float

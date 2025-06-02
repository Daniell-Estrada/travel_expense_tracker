from typing import Dict

from pydantic import BaseModel, Field, RootModel
from pydantic.root_model import RootModel


class DailyEntry(BaseModel):
    """
    Represents a daily entry in an expense report.
    This entry contains the breakdown of expenses for a specific day,
    including cash, card, and total amounts.
    """

    cash: float
    card: float
    total: float


class ReportDaily(RootModel):
    """
    Daily expense report for a trip.
    This report contains daily entries with cash, card, and total expenses.
    """

    root: Dict[str, DailyEntry] = Field(
        ...,
        description="Daily expense report with dates as keys and daily entries as values.",
    )


class ReportType(RootModel):
    """
    Expense type report for a trip.
    This report categorizes expenses by type and provides a breakdown of cash and card expenses.
    """

    root: Dict[str, DailyEntry] = Field(
        ...,
        description="Expense type report with expense types as keys and daily entries as values.",
    )


class ReportSummary(BaseModel):
    """
    Summary report for a trip.
    This report includes total expenses, total budget, remaining budget,
    trip days, and average daily expense.
    """

    total_expenses: float
    total_budget: float
    remaining_budget: float
    trip_days: int
    average_daily_expense: float

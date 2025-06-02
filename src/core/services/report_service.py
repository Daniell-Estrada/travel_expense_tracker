from collections import defaultdict
from datetime import date
from typing import Dict
from uuid import UUID

from core.enums import ExpenseType, PaymentMethod
from core.interfaces.repositories import ExpenseRepository, TripRepository


class ReportService:
    """
    Service for generating reports related to trip expenses.
    Provides methods to generate daily expense reports, expense type reports,
    and trip summaries based on expenses recorded in the system.
    """

    def __init__(
        self, expense_repository: ExpenseRepository, trip_repository: TripRepository
    ) -> None:
        """
        Initializes the ReportService with repositories for expenses and trips.
            :param expense_repository: Repository for accessing expense data.
            :param trip_repository: Repository for accessing trip data.
        """
        self._expense_repository = expense_repository
        self._trip_repository = trip_repository

    def generate_daily_expense_report(
        self, trip_id: UUID
    ) -> Dict[date, Dict[str, float]]:
        """
        Generates a daily expense report for a trip.
            :param trip_id: Unique identifier for the trip.
            :return: Dictionary with dates as keys and payment method breakdown as values.
        """
        expenses = self._expense_repository.get_by_trip_id(trip_id)
        daily_report = defaultdict(lambda: {"cash": 0.0, "card": 0.0, "total": 0.0})

        for expense in expenses:
            expense_date = expense.expense_date
            amount = expense.converted_amount_cop

            if expense.payment_method == PaymentMethod.CASH:
                daily_report[expense_date]["cash"] += amount
            else:
                daily_report[expense_date]["card"] += amount

            daily_report[expense_date]["total"] += amount

        return dict(daily_report)

    def generate_expense_type_report(
        self, trip_id: UUID
    ) -> Dict[ExpenseType, Dict[str, float]]:
        """
        Generates a report of expenses categorized by type for a trip.
            :param trip_id: Unique identifier for the trip.
            :return: Dictionary with expense types as keys and payment method breakdown as values.
        """
        expenses = self._expense_repository.get_by_trip_id(trip_id)
        type_report = defaultdict(lambda: {"cash": 0.0, "card": 0.0, "total": 0.0})

        for expense in expenses:
            expense_type = expense.expense_type
            amount = expense.converted_amount_cop

            if expense.payment_method == PaymentMethod.CASH:
                type_report[expense_type]["cash"] += amount
            else:
                type_report[expense_type]["card"] += amount

            type_report[expense_type]["total"] += amount

        return dict(type_report)

    def get_trip_summary(self, trip_id: UUID) -> Dict[str, float]:
        """
        Generates a summary of expenses for a trip, including total expenses,
        total budget, remaining budget, trip days, and average daily expense.
            :param trip_id: Unique identifier for the trip.
            :return: Dictionary containing summary statistics for the trip.
        """
        trip = self._trip_repository.get_by_id(trip_id)
        expenses = self._expense_repository.get_by_trip_id(trip_id)

        total_expenses = sum(expense.converted_amount_cop for expense in expenses)
        trip_days = (trip.end_date - trip.start_date).days + 1
        total_budget = trip.daily_budget * trip_days

        return {
            "total_expenses": total_expenses,
            "total_budget": total_budget,
            "remaining_budget": total_budget - total_expenses,
            "trip_days": trip_days,
            "average_daily_expense": total_expenses / trip_days if trip_days > 0 else 0,
        }

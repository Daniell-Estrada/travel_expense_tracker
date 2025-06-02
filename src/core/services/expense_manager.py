from datetime import date
from uuid import UUID, uuid4

from application.dto import ExpenseDTO
from core.domain import Expense
from core.exceptions import InactiveTripError
from core.interfaces import CurrencyConverter
from core.interfaces.repositories import ExpenseRepository, TripRepository


class ExpenseManager:
    """
    Manages expenses for trips, including registering expenses
    and calculating daily budget differences.
    """

    def __init__(
        self,
        expense_repository: ExpenseRepository,
        trip_repository: TripRepository,
        currency_converter: CurrencyConverter,
    ) -> None:
        """
        Initializes the ExpenseManager with repositories and a currency converter.
            :param expense_repository: Repository for managing expenses.
            :param trip_repository: Repository for managing trips.
            :param currency_converter: Service for converting currencies.
        """
        self._expense_repository: ExpenseRepository = expense_repository
        self._trip_repository: TripRepository = trip_repository
        self._currency_converter: CurrencyConverter = currency_converter

    def register_expense(self, expense_dto: ExpenseDTO) -> float:
        """
        Registers a new expense for a trip and calculates the daily budget difference.
            :param expense_dto: Data Transfer Object containing expense details.
            :return: The daily budget difference after registering the expense.
            Raises:
            InactiveTripError: If the trip associated with the expense is not active.
        """
        trip = self._trip_repository.get_by_id(expense_dto.trip_id)

        if trip and not trip.is_active():
            raise InactiveTripError()

        expense = Expense(
            expense_id=uuid4(),
            trip_id=expense_dto.trip_id,
            expense_date=expense_dto.expense_date,
            original_amount=expense_dto.amount,
            payment_method=expense_dto.payment_method,
            expense_type=expense_dto.expense_type,
        )

        if trip.is_international:
            converted_amount = self._currency_converter.convert(
                expense_dto.amount, trip.currency, "COP"
            )
            expense.converted_amount_cop = converted_amount
        else:
            expense.converted_amount_cop = expense_dto.amount

        self._expense_repository.save(expense)
        return self.calculate_daily_difference(expense.trip_id, expense.expense_date)

    def calculate_daily_difference(self, trip_id: UUID, expense_date: date) -> float:
        """
        Calculates the daily budget difference for a trip on a specific date.
            :param trip_id: Unique identifier for the trip.
            :param expense_date: Date for which to calculate the daily budget difference.
            :return: The difference between the daily budget and total expenses for that date.
            Raises:
            InactiveTripError: If the trip is not active.
        """
        trip = self._trip_repository.get_by_id(trip_id)

        if not trip or not trip.is_active():
            raise InactiveTripError()

        daily_budget = trip.daily_budget
        expenses = self._expense_repository.get_by_trip_and_date(trip_id, expense_date)

        total_expenses = sum(expense.converted_amount_cop for expense in expenses)
        daily_difference = daily_budget - total_expenses

        return daily_difference

    def get_expenses_by_trip_id(self, trip_id: UUID) -> list[Expense]:
        """
        Retrieves all expenses associated with a specific trip.
            :param trip_id: Unique identifier for the trip.
            :return: List of Expense objects for the specified trip.
        """
        return self._expense_repository.get_by_trip_id(trip_id)

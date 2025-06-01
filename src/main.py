from datetime import date
from uuid import uuid4

from application.dto import ExpenseDTO
from core.domain import Expense, Trip
from core.enums import ExpenseType, PaymentMethod
from core.services import ExpenseManager
from infrastructure.external.api_currency_converter import ApiCurrencyConverter


def main():
    """
    Main function demonstrating the expense tracking system.
    """

    # Mock repositories for demonstration
    # In a real application, these would be actual database implementations
    class MockTripRepository:
        def __init__(self):
            self.trips = {}

        def get_by_id(self, trip_id):
            return self.trips.get(trip_id)

        def save(self, trip):
            self.trips[trip._trip_id] = trip

    class MockExpenseRepository:
        def __init__(self):
            self.expenses = []

        def save(self, expense):
            self.expenses.append(expense)

        def get_by_trip_and_date(self, trip_id, expense_date):
            return [
                e
                for e in self.expenses
                if e.trip_id == trip_id and e.expense_date == expense_date
            ]

    # Initialize repositories and services
    trip_repo = MockTripRepository()
    expense_repo = MockExpenseRepository()
    currency_converter = ApiCurrencyConverter()

    expense_manager = ExpenseManager(
        expense_repository=expense_repo,
        trip_repository=trip_repo,
        currency_converter=currency_converter,
    )

    # Create a sample trip
    trip_id = uuid4()
    trip = Trip(
        trip_id=trip_id,
        start_date=date.today(),
        end_date=date(2025, 12, 31),
        is_international=False,
        daily_budget=100000.0,
        currency="COP",
    )
    trip_repo.save(trip)

    # Create and register an expense
    expense_dto = ExpenseDTO(
        trip_id=trip_id,
        expense_date=date.today(),
        amount=50000.0,
        payment_method=PaymentMethod.CARD,
        expense_type=ExpenseType.FOOD,
    )

    try:
        daily_difference = expense_manager.register_expense(expense_dto)
        print(f"Expense registered successfully!")
        print(f"Daily budget difference: ${daily_difference:,.2f} COP")
    except Exception as e:
        print(f"Error registering expense: {e}")


if __name__ == "__main__":
    main()

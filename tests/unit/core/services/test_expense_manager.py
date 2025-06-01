from datetime import date
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4

from src.application.dto import ExpenseDTO
from src.core.domain import Expense, Trip
from src.core.enums import ExpenseType, PaymentMethod
from src.core.exceptions import InactiveTripError, TripNotFoundError
from src.core.services import ExpenseManager


class TestExpanseManager(TestCase):
    """Test case for ExpenseManager class."""

    def __init__(self, methodName: str = "runTest") -> None:
        """
        Initializes the test case with mock repositories and a manager instance.
        """

        super().__init__(methodName)
        self.mock_expense_repo = MagicMock()
        self.mock_trip_repo = MagicMock()
        self.mock_converter = MagicMock()
        self.manager = ExpenseManager(
            expense_repository=self.mock_expense_repo,
            trip_repository=self.mock_trip_repo,
            currency_converter=self.mock_converter,
        )

    def test_domestic_trip_success(self):
        """
        Tests the registration of an expense for a domestic trip.
        """
        domestic_trip = Trip(
            trip_id=uuid4(),
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 10),
            is_international=False,
            daily_budget=500000,
            currency="COP",
        )

        dto = ExpenseDTO(
            trip_id=domestic_trip.trip_id,
            expense_date=date(2025, 6, 5),
            amount=350000,
            payment_method=PaymentMethod.CARD,
            expense_type=ExpenseType.TRANSPORTATION,
        )

        expense = Expense(
            expense_id=uuid4(),
            trip_id=domestic_trip.trip_id,
            expense_date=dto.expense_date,
            original_amount=dto.amount,
            currency=domestic_trip.currency,
            converted_amount_cop=dto.amount,
            payment_method=dto.payment_method,
            expense_type=dto.expense_type,
        )

        self.mock_trip_repo.get_by_id.return_value = domestic_trip
        self.mock_expense_repo.get_by_trip_and_date.return_value = [expense]

        result = self.manager.register_expense(dto)

        self.assertEqual(result, 150000)
        self.mock_expense_repo.save.assert_called_once()
        saved_expense = self.mock_expense_repo.save.call_args[0][0]
        self.assertEqual(saved_expense.converted_amount_cop, 350000)
        self.mock_converter.convert.assert_not_called()

    def test_international_trip_success(self):
        """
        Tests the registration of an expense for an international trip.
        """
        international_trip = Trip(
            trip_id=uuid4(),
            start_date=date(2025, 5, 30),
            end_date=date(2025, 6, 10),
            is_international=True,
            daily_budget=500000,
            currency="USD",
        )
        dto = ExpenseDTO(
            trip_id=international_trip.trip_id,
            expense_date=date(2025, 6, 5),
            amount=50,
            payment_method=PaymentMethod.CARD,
            expense_type=ExpenseType.TRANSPORTATION,
        )

        expense = Expense(
            expense_id=uuid4(),
            trip_id=international_trip.trip_id,
            expense_date=dto.expense_date,
            original_amount=dto.amount,
            currency=international_trip.currency,
            converted_amount_cop=0,  # Will be set after conversion
            payment_method=dto.payment_method,
            expense_type=dto.expense_type,
        )

        self.mock_trip_repo.get_by_id.return_value = international_trip
        self.mock_converter.convert.return_value = 200000
        expense.converted_amount_cop = self.mock_converter.convert(
            dto.amount, international_trip.currency, "COP"
        )
        self.mock_expense_repo.get_by_trip_and_date.return_value = [expense]

        result = self.manager.register_expense(dto)

        self.assertEqual(result, 300000)
        saved_expense = self.mock_expense_repo.save.call_args[0][0]
        self.assertEqual(saved_expense.converted_amount_cop, 200000)

    def test_inactive_trip_error(self):
        """
        Tests that an InactiveTripError is raised when trying to register
        an expense for an inactive trip.
        """

        inactive_trip = Trip(
            uuid4(), date(2025, 1, 1), date(2025, 1, 10), False, 500000, "COP"
        )
        dto = ExpenseDTO(
            trip_id=inactive_trip.trip_id,
            expense_date=date(2025, 6, 5),
            amount=350000,
            payment_method=PaymentMethod.CARD,
            expense_type=ExpenseType.TRANSPORTATION,
        )
        self.mock_trip_repo.get_by_id.return_value = inactive_trip

        with self.assertRaises(InactiveTripError):
            self.manager.register_expense(dto)
        self.mock_expense_repo.save.assert_not_called()

    def test_trip_not_found(self):
        """
        Tests that a TripNotFoundError is raised when the trip does not exist.
        """

        trip_id = uuid4()

        dto = ExpenseDTO(
            trip_id=trip_id,
            expense_date=date(2025, 6, 5),
            amount=350000,
            payment_method=PaymentMethod.CARD,
            expense_type=ExpenseType.TRANSPORTATION,
        )

        self.mock_trip_repo.get_by_id.side_effect = TripNotFoundError(trip_id)

        with self.assertRaises(TripNotFoundError):
            self.manager.register_expense(dto)
        self.mock_expense_repo.save.assert_not_called()

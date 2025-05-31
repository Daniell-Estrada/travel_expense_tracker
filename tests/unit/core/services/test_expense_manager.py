from datetime import date
from unittest import TestCase
from unittest.mock import MagicMock, patch

from application.dto.expense_dto import ExpenseDTO
from core.enums import ExpenseType, PaymentMethod
from core.services.expense_manager import ExpenseManager

from core.domain.exceptions import InactiveTripError
from core.domain.trip import Trip


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
            expense_repo=self.mock_expense_repo,
            trip_repo=self.mock_trip_repo,
            converter=self.mock_converter,
        )

        self.domestic_trip = Trip(
            1, date(2025, 6, 1), date(2025, 6, 10), False, 500000, "COP"
        )

        self.international_trip = Trip(
            2, date(2025, 7, 1), date(2025, 7, 10), True, 200, "USD"
        )

        self.expense_dto = ExpenseDTO(
            trip_id=1,
            date=date(2023, 6, 5),
            amount=150000,
            payment_method=PaymentMethod.CARD,
            expense_type=ExpenseType.TRANSPORTATION,
        )

    def test_domestic_trip_success(self):
        """
        Tests the registration of an expense for a domestic trip.
        """
        self.mock_trip_repo.get_by_id.return_value = self.domestic_trip
        self.mock_expense_repo.get_by_trip_id.return_value = []

        result = self.manager.register_expense(self.expense_dto)

        self.assertEqual(result, 350000)
        self.mock_expense_repo.save.assert_called_once()
        saved_expense = self.mock_expense_repo.save.call_args[0][0]
        assert saved_expense.converted_amount_cop == 150000
        self.mock_converter.convert.assert_not_called()

    def test_international_trip_success(self):
        """
        Tests the registration of an expense for an international trip.
        """
        dto = self.expense_dto.copy()
        dto.trip_id = 2
        dto.amount = 50  # USD
        self.mock_trip_repo.get_by_id.return_value = self.international_trip
        self.mock_converter.convert.return_value = 200000  # 50 USD = 200,000 COP
        self.mock_expense_repo.get_by_trip_and_date.return_value = []

        # Ejecutar
        result = self.manager.register_expense(dto)

        # Verificar
        self.assertEqual(result, 300000)
        self.mock_converter.convert.assert_called_once_with(50, "USD", "COP")
        saved_expense = self.mock_expense_repo.save.call_args[0][0]
        self.assertEqual(saved_expense.converted_amount_cop, 200000)

    def test_inactive_trip_error(self):
        """
        Tests that an InactiveTripError is raised when trying to register
        an expense for an inactive trip.
        """

        inactive_trip = self.domestic_trip.copy()
        inactive_trip.end_date = date(2025, 6, 2)  # Viaje terminado
        self.mock_trip_repo.get_by_id.return_value = inactive_trip

        with self.assertRaises(InactiveTripError):
            self.manager.register_expense(self.expense_dto)
        self.mock_expense_repo.save.assert_not_called()

    def test_currency_conversion_failure(self):
        """
        Tests that an exception is raised if currency conversion fails.
        """

        dto = self.expense_dto.copy()
        dto.trip_id = 2
        self.mock_trip_repo.get_by_id.return_value = self.international_trip
        self.mock_converter.convert.side_effect = ConversionError("API failure")

        # Verificar
        with self.assertRaises(ConversionError):
            self.manager.register_expense(dto)
        self.mock_expense_repo.save.assert_not_called()

    def test_trip_not_found(self):
        """
        Tests that a TripNotFoundError is raised when the trip does not exist.
        """

        self.mock_trip_repo.get_by_id.side_effect = TripNotFoundError()

        with self.assertRaises(TripNotFoundError):
            self.manager.register_expense(self.expense_dto)
        self.mock_expense_repo.save.assert_not_called()

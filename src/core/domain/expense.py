from datetime import date
from uuid import UUID

from src.core.enums import ExpenseType, PaymentMethod


class Expense:
    """
    Represents an expense incurred during a trip,
    including details such as date, amount, currency, and type.
    """

    def __init__(
        self,
        expense_id: UUID,
        trip_id: UUID,
        expense_date: date,
        original_amount: float,
        currency: str = "COP",
        converted_amount_cop: float = 0.0,
        payment_method: PaymentMethod = PaymentMethod.CASH,
        expense_type: ExpenseType = ExpenseType.OTHER,
    ):
        """
        Initializes an Expense instance.
            :param expense_id: Unique identifier for the expense.
            :param trip_id: Identifier for the trip associated with the expense.
            :param expense_date: Date of the expense.
            :param original_amount: Original amount of the expense in the specified currency.
            :param currency: Currency of the original amount.
            :param converted_amount: Amount converted to the trip's currency.
            :param payment_method: Method of payment used for the expense.
            :param expense_type: Type of the expense (e.g., food, transportation).
        """

        self._expense_id: UUID = expense_id
        self._trip_id: UUID = trip_id
        self._expense_date: date = expense_date
        self._original_amount: float = original_amount
        self._currency: str = currency
        self._converted_amount_cop: float = converted_amount_cop
        self._payment_method: PaymentMethod = payment_method
        self._expense_type: ExpenseType = expense_type

    @property
    def trip_id(self) -> UUID:
        """
        Returns the trip ID associated with the expense.
            :return: Unique identifier for the trip.
        """
        return self._trip_id

    @property
    def expense_date(self) -> date:
        """
        Returns the date of the expense.
            :return: Date of the expense.
        """
        return self._expense_date

    @property
    def converted_amount_cop(self) -> float:
        """
        Returns the converted amount for the expense.
            :return: Amount converted to the trip's currency.
        """
        return self._converted_amount_cop

    @converted_amount_cop.setter
    def converted_amount_cop(self, value: float) -> None:
        """
        Sets the converted amount for the expense.
            :param value: Amount converted to the trip's currency.
        """
        self._converted_amount_cop = value

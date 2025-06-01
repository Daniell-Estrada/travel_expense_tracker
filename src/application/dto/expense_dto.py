from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.core.enums import ExpenseType, PaymentMethod


@dataclass
class ExpenseDTO:
    """
    Data Transfer Object for Expense.
    Represents an expense with details such as trip ID, date, amount, payment method, and type.
    """

    trip_id: UUID
    expense_date: date
    amount: float
    payment_method: PaymentMethod
    expense_type: ExpenseType

"""
Modelos de request/response para Expense endpoints.
"""

from dataclasses import dataclass
from datetime import date
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from core.enums import ExpenseType, PaymentMethod


class ExpenseCreateRequest(BaseModel):
    """Model for creating a new Expense."""

    trip_id: UUID = Field(
        ..., description="trip_id of the trip associated with the expense"
    )
    expense_date: date = Field(..., description="Date of the expense")
    amount: float = Field(
        ..., gt=0, description="Amount of the expense in the trip's currency"
    )
    expense_type: ExpenseType = Field(..., description="Type of the expense")
    payment_method: PaymentMethod = Field(
        ..., description="Payment method used for the expense"
    )


class ExpenseResponse(BaseModel):
    """Model for returning Expense details."""

    trip_id: UUID
    expense_id: UUID
    expense_date: date
    amount: float
    converted_amount: float
    payment_method: PaymentMethod
    expense_type: ExpenseType

    @dataclass
    class Config:
        """Configuration for the ExpenseResponse model."""

        from_attributes = True


class ExpenseCreateResponse(BaseModel):
    """Model for returning the result of creating an Expense."""

    message: str
    daily_difference: float
    status: str


class ExpenseListResponse(BaseModel):
    """Model for returning a list of Expenses."""

    expenses: List[ExpenseResponse]
    total_amount: float
    total_count: int

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from application.dto import ExpenseDTO
from core.exceptions import InactiveTripError, TripNotFoundError
from core.services import ExpenseManager
from presentation.api.dependencies import DependencyContainer
from presentation.api.models import (ExpenseCreateRequest,
                                     ExpenseCreateResponse, ExpenseResponse)


class ExpenseController:
    """
    Controller for managing expense-related endpoints.
    Provides methods to create and retrieve expenses for trips.
        - create_expense: Creates a new expense with the provided details.
        - get_all_expenses: Retrieves all expenses for a specific trip.
    """

    def __init__(self, expense_service: ExpenseManager) -> None:
        self._expense_service: ExpenseManager = expense_service

    async def create_expense(
        self, expense_data: ExpenseCreateRequest
    ) -> ExpenseCreateResponse:
        """
        Create a new expense with the provided details.
            :param expense_data: ExpenseCreateRequest containing expense details.
            :return: ExpenseCreateResponse containing the created expense details.
            :raises HTTPException: If the trip is inactive or not found.
        """
        try:
            expense_dto = ExpenseDTO(
                trip_id=expense_data.trip_id,
                expense_date=expense_data.expense_date,
                amount=expense_data.amount,
                expense_type=expense_data.expense_type,
                payment_method=expense_data.payment_method,
            )

            daily_difference = self._expense_service.register_expense(expense_dto)

            if daily_difference < 0:
                status_message = "over_budget"
            elif daily_difference == 0:
                status_message = "exact_budget"
            else:
                status_message = "within_budget"

            return ExpenseCreateResponse(
                message="Expense created successfully",
                daily_difference=daily_difference,
                status=status_message,
            )
        except InactiveTripError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add expenses to an inactive trip",
            ) from e
        except TripNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error registering expense: {str(e)}",
            ) from e

    async def get_all_expenses(self, trip_id: UUID) -> List[ExpenseResponse]:
        """
        Get all expenses for a specific trip.
            :param trip_id: UUID of the trip to retrieve expenses for.
            :return: List of ExpenseResponse containing all expenses for the trip.
            :raises HTTPException: If the trip is not found or an error occurs.
        """
        try:
            expenses = self._expense_service.get_expenses_by_trip_id(trip_id)

            return [
                ExpenseResponse(
                    trip_id=expense.trip_id,
                    expense_id=expense.expense_id,
                    expense_date=expense.expense_date,
                    amount=expense.original_amount,
                    converted_amount=expense.converted_amount_cop,
                    payment_method=expense.payment_method,
                    expense_type=expense.expense_type,
                )
                for expense in expenses
            ]
        except TripNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving expenses: {str(e)}",
            ) from e


router = APIRouter(prefix="/expenses", tags=["expenses"])
expense_controller = ExpenseController(
    expense_service=DependencyContainer().get_expense_manager()
)

router.add_api_route(
    "/",
    expense_controller.create_expense,
    methods=["POST"],
    response_model=ExpenseCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Expense",
    description="Create a new expense for a trip",
)

router.add_api_route(
    "/{trip_id}",
    expense_controller.get_all_expenses,
    methods=["GET"],
    response_model=List[ExpenseResponse],
    summary="Get All Expenses",
    description="Retrieve all expenses for a specific trip",
)

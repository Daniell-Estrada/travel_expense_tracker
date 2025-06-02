from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from core.exceptions import TripNotFoundError
from core.services import ReportService
from presentation.api.dependencies import DependencyContainer
from presentation.api.models import ReportDaily, ReportSummary, ReportType


class ReportController:
    """
    Controller for managing report-related endpoints.
    This controller provides methods to generate and retrieve reports for trips.
        - get_trip_report: Generates a report for a specific trip.
    """

    def __init__(self, report_service: ReportService) -> None:
        """
        Initialize the ReportController with dependencies.
            :param report_service: Service to manage reports.
        """
        self._report_service: ReportService = report_service

    async def get_daily_report(self, trip_id: UUID) -> ReportDaily:
        """
        Generates a daily expense report for a trip.
            :param trip_id: Unique identifier for the trip.
            :return: A ReportDaily object containing the daily expense report.
            :raises HTTPException: If the trip is not found or an error generating the report.
        """
        try:
            report = self._report_service.generate_daily_expense_report(trip_id)

            serialized_report = {str(date): entry for date, entry in report.items()}
            return ReportDaily.model_validate(serialized_report)

        except TripNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating report: {str(e)}",
            ) from e

    async def get_type_report(self, trip_id: UUID) -> ReportType:
        """
        Generates a report of expenses categorized by type for a trip.
            :param trip_id: Unique identifier for the trip.
            :return: A dictionary containing the expense type report.
            :raises HTTPException: If the trip is not found or an error generating the report.
        """
        try:
            report = self._report_service.generate_expense_type_report(trip_id)
            serialized_report = {
                str(expense_type): entry for expense_type, entry in report.items()
            }
            return ReportType.model_validate(serialized_report)

        except TripNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating report: {str(e)}",
            ) from e

    async def get_trip_summary(self, trip_id: UUID) -> ReportSummary:
        """
        Generates a  summary report for a trip.
            :param trip_id: Unique identifier for the trip.
            :return: A ReportSummary object containing the trip summary.
            :raises HTTPException: If the trip is not found or an error generating the report.
        """
        try:
            summary = self._report_service.get_trip_summary(trip_id)
            return ReportSummary.model_validate(summary)

        except TripNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating report: {str(e)}",
            ) from e


router = APIRouter(prefix="/reports", tags=["reports"])
report_controller = ReportController(
    report_service=DependencyContainer().get_report_service()
)

router.add_api_route(
    "/daily/{trip_id}",
    report_controller.get_daily_report,
    methods=["GET"],
    response_model=ReportDaily,
    summary="Get daily expense report for a trip.",
    description="Generates a daily expense report for a trip, including cash and card expenses.",
)

router.add_api_route(
    "/type/{trip_id}",
    report_controller.get_type_report,
    methods=["GET"],
    response_model=ReportType,
    summary="Get expense type report for a trip.",
    description="Generates a report of expenses categorized by type for a trip.",
)

router.add_api_route(
    "/summary/{trip_id}",
    report_controller.get_trip_summary,
    methods=["GET"],
    response_model=ReportSummary,
    summary="Get trip summary report.",
    description="Generates a summary report for a trip, including total expenses.",
)

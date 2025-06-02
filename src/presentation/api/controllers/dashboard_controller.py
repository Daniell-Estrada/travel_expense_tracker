from fastapi import APIRouter, HTTPException, status

from core.services import ReportService, TripService
from presentation.api.dependencies import DependencyContainer
from presentation.api.models import (DashboardStatsResponse, TripListResponse,
                                     TripResponse)


class DashboardController:
    """
    Controller for managing dashboard-related endpoints.
    This controller provides methods to retrieve dashboard statistics and active trips.
        - get_dashboard_stats: Retrieves statistics for the dashboard.
        - get_active_trips: Retrieves a list of active trips.
    """

    def __init__(
        self, trip_service: TripService, report_service: ReportService
    ) -> None:
        """
        Initialize the DashboardController with dependencies.
            :param trip_service: Service to manage trips.
            :param report_service: Service to manage reports.
        """
        self._trip_service: TripService = trip_service
        self._report_service: ReportService = report_service

    async def get_dashboard_stats(self) -> DashboardStatsResponse:
        """
        Get dashboard statistics including total trips, active trips, and total expenses.
            :return: Dictionary containing dashboard statistics.
        """
        try:
            all_trips = self._trip_service.get_all_trips()
            active_trips = [trip for trip in all_trips if trip.is_active()]

            total_expenses = 0
            total_days = 0

            for trip in all_trips:
                try:
                    summary = self._report_service.get_trip_summary(trip.trip_id)
                    total_expenses += summary["total_expenses"]
                    total_days += summary["trip_days"]
                except Exception as e:
                    raise e

            avg_daily_expense = total_expenses / total_days if total_days > 0 else 0

            return DashboardStatsResponse(
                total_trips=len(all_trips),
                active_trips=len(active_trips),
                total_expenses=total_expenses,
                avg_daily_expense=avg_daily_expense,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving dashboard statistics: {str(e)}",
            ) from e

    async def get_active_trips(self) -> TripListResponse:
        """
        Get a list of active trips.
            :return: TripListResponse containing active trips.
        """
        try:
            trips = self._trip_service.get_active_trips()
            trip_responses = [
                TripResponse(
                    trip_id=trip.trip_id,
                    start_date=trip.start_date,
                    end_date=trip.end_date,
                    is_international=trip.is_international,
                    daily_budget=trip.daily_budget,
                    currency=trip.currency,
                    is_active=trip.is_active(),
                )
                for trip in trips
            ]
            return TripListResponse(trips=trip_responses, total=len(trip_responses))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving active trips",
            ) from e


router = APIRouter(prefix="/dashboard", tags=["dashboard"])

dashboard_controller = DashboardController(
    trip_service=DependencyContainer().get_trip_service(),
    report_service=DependencyContainer().get_report_service(),
)

router.add_api_route(
    "/stats",
    dashboard_controller.get_dashboard_stats,
    methods=["GET"],
    response_model=DashboardStatsResponse,
    summary="Get Dashboard Statistics",
    description="Retrieve statistics for the dashboard.",
)

router.add_api_route(
    "/active-trips",
    dashboard_controller.get_active_trips,
    methods=["GET"],
    response_model=TripListResponse,
    summary="Get Active Trips",
    description="Retrieve a list of active trips.",
)

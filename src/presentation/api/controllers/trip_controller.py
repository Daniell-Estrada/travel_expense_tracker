from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from core.services import TripService
from presentation.api.dependencies import DependencyContainer
from presentation.api.models.trip_models import (TripCreateRequest,
                                                 TripListResponse,
                                                 TripResponse)


class TripController:
    """
    Controller for managing trip-related endpoints.
    Provides methods to create, retrieve, and manage trips.
        - create_trip: Creates a new trip with the provided details.
        - get_all_trips: Retrieves all trips, optionally filtering by active status.
        - get_trip_by_id: Retrieves
            a trip by its unique identifier.
    """

    def __init__(self, trip_service: TripService) -> None:
        self._trip_service: TripService = trip_service

    async def create_trip(self, trip_data: TripCreateRequest) -> TripResponse:
        """
        Create a new trip with the provided details.
            :param trip_data: TripCreateRequest containing trip details.
            :return: TripResponse containing the created trip details.
            :raises HTTPException: If the trip data is invalid.
        """
        try:
            trip = self._trip_service.create_trip(
                start_date=trip_data.start_date,
                end_date=trip_data.end_date,
                is_international=trip_data.is_international,
                daily_budget=trip_data.daily_budget,
                currency=trip_data.currency,
            )

            return TripResponse(
                trip_id=trip.trip_id,
                start_date=trip.start_date,
                end_date=trip.end_date,
                is_international=trip.is_international,
                daily_budget=trip.daily_budget,
                currency=trip.currency,
                is_active=trip.is_active(),
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            ) from e

    async def get_all_trips(self, active_only: bool = False) -> TripListResponse:
        """
        Get all trips, optionally filtering by active status.
            :param active_only: If True, only returns active trips.
            :return: TripListResponse containing a list of trips and total count.
        """
        try:
            if active_only:
                trips = self._trip_service.get_active_trips()
            else:
                trips = self._trip_service.get_all_trips()

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
                detail="An error occurred while retrieving trips",
            ) from e

    async def get_trip_by_id(self, trip_id: UUID) -> TripResponse:
        """
        Get a trip by its unique identifier.
            :param trip_id: Unique identifier for the trip.
            :return: TripResponse containing trip details.
            :raises HTTPException: If the trip is not found.
        """
        try:
            trip = self._trip_service.get_trip_by_id(trip_id)

            return TripResponse(
                trip_id=trip.trip_id,
                start_date=trip.start_date,
                end_date=trip.end_date,
                is_international=trip.is_international,
                daily_budget=trip.daily_budget,
                currency=trip.currency,
                is_active=trip.is_active(),
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            ) from e


router = APIRouter(prefix="/trips", tags=["trips"])

trip_controller = TripController(trip_service=DependencyContainer().get_trip_service())

router.add_api_route(
    "/",
    trip_controller.create_trip,
    methods=["POST"],
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new trip",
    description="Create a new trip with the provided details",
)

router.add_api_route(
    "/",
    trip_controller.get_all_trips,
    methods=["GET"],
    response_model=TripListResponse,
    summary="Get all trips",
    description="Retrieve all trips with optional filtering",
)

router.add_api_route(
    "/{trip_id}",
    trip_controller.get_trip_by_id,
    methods=["GET"],
    response_model=TripResponse,
    summary="Get trip by ID",
    description="Retrieve a trip by its unique identifier",
)

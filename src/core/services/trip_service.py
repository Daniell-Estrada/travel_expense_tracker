from datetime import date
from typing import List
from uuid import UUID, uuid4

from core.domain import Trip
from core.interfaces.repositories import TripRepository


class TripService:
    """
    Service class for managing trips.
    Provides methods to create, retrieve, and manage trips.
        - create_trip: Creates a new trip with specified parameters.
        - get_trip_by_id: Retrieves a trip by its unique identifier.
        - get_all_trips: Retrieves all trips stored in the repository.
    """

    def __init__(self, trip_repository: TripRepository) -> None:
        """
        Initializes the TripService with a TripRepository instance.
            :param trip_repository: An instance of TripRepository for data persistence operations.
        """
        self._trip_repository = trip_repository

    def create_trip(
        self,
        start_date: date,
        end_date: date,
        is_international: bool,
        daily_budget: float,
        currency: str = "COP",
    ) -> Trip:
        """
        Creates a new trip with the specified parameters.
            :param start_date: Start date of the trip.
            :param end_date: End date of the trip.
            :param is_international: Indicates if the trip is international.
            :param daily_budget: Daily budget for the trip.
            :param currency: Currency for the budget, default is "COP".
            :return: The created Trip object.
            :raises ValueError: If the start date is after the end date
                or if the daily budget is negative.
        """

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        if daily_budget < 0:
            raise ValueError("Daily budget cannot be negative")

        trip = Trip(
            trip_id=uuid4(),
            start_date=start_date,
            end_date=end_date,
            is_international=is_international,
            daily_budget=daily_budget,
            currency=currency,
        )

        self._trip_repository.save(trip)
        return trip

    def get_trip_by_id(self, trip_id: UUID) -> Trip:
        """
        Retrieves a trip by its unique identifier.
            :param trip_id: Unique identifier for the trip.
            :return: Trip object corresponding to the given trip_id.
        """

        return self._trip_repository.get_by_id(trip_id)

    def get_all_trips(self) -> List[Trip]:
        """
        Retrieves all trips stored in the repository.
            :return: A list of all Trip objects.
        """
        return self._trip_repository.get_all()

    def get_active_trips(self) -> List[Trip]:
        """
        Retrieves all active trips.
            :return: A list of active Trip objects.
        """
        all_trips = self._trip_repository.get_all()
        return [trip for trip in all_trips if trip.is_active()]

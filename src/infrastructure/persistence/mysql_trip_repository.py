from typing import List
from uuid import UUID

from mysql.connector import Error

from core.domain import Trip
from core.exceptions import TripNotFoundError
from core.interfaces.repositories import TripRepository
from infrastructure.database import DatabaseConnection


class MySQLTripRepository(TripRepository):
    """
    MySQL implementation of TripRepository.
    Handles persistence operations for Trip entities.
    """

    def __init__(self, db_connection: DatabaseConnection) -> None:
        self._db_connection = db_connection

    def save(self, trip: Trip) -> None:
        """
        Saves a trip to the database.

        :param trip: Trip object to be saved.
        :raises RuntimeError: If there is an error during the database operation.
        """

        query = """
            INSERT INTO trips (trip_id, start_date, end_date, is_international, daily_budget, currency)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            with self._db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    query,
                    (
                        str(trip.trip_id),
                        trip.start_date,
                        trip.end_date,
                        trip.is_international,
                        trip.daily_budget,
                        trip.currency,
                    ),
                )
                connection.commit()
        except Error as e:
            raise RuntimeError(f"Error saving trip {trip.trip_id}: {e}") from e

    def get_by_id(self, trip_id: UUID) -> Trip:
        """
        Retrieves a trip by its unique identifier.
            :param trip_id: Unique identifier for the trip.
            :return: Trip object corresponding to the given trip_id.
        """

        query = "SELECT * FROM trips WHERE trip_id = %s"

        try:
            with self._db_connection.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (str(trip_id),))
                result = cursor.fetchone()

                if not result:
                    raise TripNotFoundError(trip_id)

                return Trip(
                    trip_id=UUID(result["trip_id"]),
                    start_date=result["start_date"],
                    end_date=result["end_date"],
                    is_international=result["is_international"],
                    daily_budget=float(result["daily_budget"]),
                    currency=result["currency"],
                )
        except Error as e:
            raise RuntimeError(f"Error retrieving trip by ID {trip_id}: {e}") from e

    def get_all(self) -> List[Trip]:
        """
        Retrieves all trips from the database.

        Returns:
            List of all Trip objects.
        """
        query = "SELECT * FROM trips ORDER BY start_date DESC"

        try:
            with self._db_connection.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query)
                results = cursor.fetchall()

                return [
                    Trip(
                        trip_id=UUID(row["trip_id"]),
                        start_date=row["start_date"],
                        end_date=row["end_date"],
                        is_international=row["is_international"],
                        daily_budget=float(row["daily_budget"]),
                        currency=row["currency"],
                    )
                    for row in results
                ]
        except Error as e:
            raise RuntimeError(f"Error retrieving trips: {e}") from e

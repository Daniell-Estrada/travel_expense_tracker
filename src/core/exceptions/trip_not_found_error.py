from uuid import UUID


class TripNotFoundError(Exception):
    """Exception raised when a trip is not found."""

    def __init__(self, trip_id: UUID):
        self.trip_id: UUID = trip_id
        super().__init__(f"Trip with ID '{self.trip_id}' not found.")

    def __str__(self):
        return f"TripNotFoundError: {self.trip_id}"

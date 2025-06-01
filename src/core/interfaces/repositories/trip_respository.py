from abc import ABC, abstractmethod
from uuid import UUID

from core.domain import Trip


class TripRepository(ABC):
    @abstractmethod
    def get_by_id(self, trip_id: UUID) -> Trip:
        """
        Retrieves a trip by its unique identifier.
            :param trip_id: Unique identifier for the trip.
            :return: Trip object corresponding to the given trip_id.
        """

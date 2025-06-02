from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from core.domain import Trip


class TripRepository(metaclass=ABCMeta):
    """
    Abstract base class for Trip repository.
    Defines the interface for interacting with trip data storage.
    """

    @classmethod
    def __subclasshook__(cls, subclass: type, /) -> bool:
        """
        Checks if a subclass is a valid TripRepository.
            :param subclass: The class to check.
            :return: True if subclass implements all abstract methods, False otherwise.
        """
        return all(
            (hasattr(subclass, method) and callable(getattr(subclass, method)))
            for method in ["save", "get_by_id", "get_all"]
        )

    @abstractmethod
    def save(self, trip: Trip) -> None:
        """
        Saves a trip to the repository.
            :param trip: The trip object to be saved.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_by_id(self, trip_id: UUID) -> Trip:
        """
        Retrieves a trip by its unique identifier.
            :param trip_id: Unique identifier for the trip.
            :return: Trip object corresponding to the given trip_id.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_all(self) -> List[Trip]:
        """
        Retrieves all trips stored in the repository.
            :return: A list of all Trip objects.
        """
        raise NotImplementedError("Subclasses must implement this method")

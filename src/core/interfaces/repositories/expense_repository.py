from abc import ABCMeta, abstractmethod
from datetime import date
from typing import List
from uuid import UUID

from core.domain import Expense

class ExpenseRepository(metaclass=ABCMeta):
    """
    Abstract base class for Expense repository.
    Defines the interface for interacting with expense data storage.
    """

    @classmethod
    def __subclasshook__(cls, subclass: type, /) -> bool:
        """
        Checks if a subclass is a valid ExpenseRepository.
            :param subclass: The class to check.
            :return: True if subclass implements all abstract methods, False otherwise.
        """
        return all(
            (hasattr(subclass, method) and callable(getattr(subclass, method)))
            for method in ["save", "get_by_trip_id", "get_by_trip_and_date"]
        )

    @abstractmethod
    def save(self, expense: Expense) -> None:
        """
        Saves an expense to the repository.
            :param expense: The expense object to be saved.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_by_trip_id(self, trip_id: UUID) -> List[Expense]:
        """
        Retrieves all expenses for a specific trip.
            :param trip_id: Unique identifier for the trip.
            :return: List of Expense objects for the given trip_id.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_by_trip_and_date(self, trip_id: UUID, expense_date: date) -> List[Expense]:
        """
        Retrieves an expense by trip ID and date.
            :param trip_id: Unique identifier for the trip.
            :param date: Date of the expense in 'YYYY-MM-DD' format.
            :return: Expense object corresponding to the given trip_id and date.
        """
        raise NotImplementedError("Subclasses must implement this method")

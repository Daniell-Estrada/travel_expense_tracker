from abc import ABC, abstractmethod
from datetime import date
from typing import List
from uuid import UUID

from src.core.domain import Expense


class ExpenseRepository(ABC):
    """
    Abstract base class for Expense repository.
    Defines the interface for interacting with expense data storage.
    """

    @abstractmethod
    def save(self, expense: Expense) -> None:
        """
        Saves an expense to the repository.
            :param expense: The expense object to be saved.
        """

    @abstractmethod
    def get_by_trip_and_date(self, trip_id: UUID, expense_date: date) -> List[Expense]:
        """
        Retrieves an expense by trip ID and date.
            :param trip_id: Unique identifier for the trip.
            :param date: Date of the expense in 'YYYY-MM-DD' format.
            :return: Expense object corresponding to the given trip_id and date.
        """

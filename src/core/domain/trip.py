from datetime import date
from uuid import UUID


class Trip:
    """
    Represents a trip with details such as start and end dates, budget, and currency.
    """

    def __init__(
        self,
        trip_id: UUID,
        start_date: date,
        end_date: date,
        is_international: bool,
        daily_budget: float,
        currency: str = "COP",
    ):
        """
        Initializes a Trip instance.
            :param id: Unique identifier for the trip.
            :param start_date: Start date of the trip.
            :param end_date: End date of the trip.
            :param is_international: Indicates if the trip is international.
            :param daily_budget: Daily budget for the trip.
            :param currency: Currency for the budget, default is "COP".
        """

        self._trip_id: UUID = trip_id
        self._start_date: date = start_date
        self._end_date: date = end_date
        self._is_international: bool = is_international
        self._daily_budget: float = daily_budget
        self._currency: str = currency

    @property
    def trip_id(self) -> UUID:
        """
        Returns the unique identifier of the trip.
            :return: UUID of the trip.
        """
        return self._trip_id

    @property
    def start_date(self) -> date:
        """
        Returns the start date of the trip.
            :return: Start date as a date object.
        """
        return self._start_date

    @property
    def end_date(self) -> date:
        """
        Returns the end date of the trip.
            :return: End date as a date object.
        """
        return self._end_date

    @property
    def is_international(self) -> bool:
        """
        Indicates if the trip is international.
            :return: True if the trip is international, False otherwise.
        """
        return self._is_international

    @property
    def daily_budget(self) -> float:
        """
        Returns the daily budget for the trip.
            :return: Daily budget as a float.
        """
        return self._daily_budget

    @property
    def currency(self) -> str:
        """
        Returns the currency of the trip.
            :return: Currency code as a string.
        """
        return self._currency

    def is_active(self) -> bool:
        """
        Checks if the trip is currently active based on the start and end dates.
            :return: True if the trip is active, False otherwise.
        """
        today = date.today()
        return self._start_date <= today <= self._end_date

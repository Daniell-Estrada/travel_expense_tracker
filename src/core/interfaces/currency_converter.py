from abc import ABC, abstractmethod


class CurrencyConverter(ABC):
    """
    Abstract base class for currency conversion.
    Defines the interface for converting amounts between different currencies.
    """

    @abstractmethod
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Converts an amount from one currency to another.
            :param amount: The amount of money to convert.
            :param from_currency: The currency code of the original amount (e.g., 'USD').
            :param to_currency: The currency code to convert the amount into (e.g., 'EUR').
            :return: The converted amount in the target currency.
        """

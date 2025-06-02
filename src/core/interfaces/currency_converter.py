from abc import ABCMeta, abstractmethod


class CurrencyConverter(metaclass=ABCMeta):
    """
    Abstract base class for currency conversion.
    Defines the interface for converting amounts between different currencies.
    """

    @classmethod
    def __subclasshook__(cls, subclass: type, /) -> bool:
        """
        Checks if a subclass is a valid CurrencyConverter.
            :param subclass: The class to check.
            :return: True if subclass implements all abstract methods, False otherwise.
        """
        return all(
            (hasattr(subclass, method) and callable(getattr(subclass, method)))
            for method in ["convert"]
        )

    @abstractmethod
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Converts an amount from one currency to another.
            :param amount: The amount of money to convert.
            :param from_currency: The currency code of the original amount (e.g., 'USD').
            :param to_currency: The currency code to convert the amount into (e.g., 'EUR').
            :return: The converted amount in the target currency.
        """
        raise NotImplementedError("Subclasses must implement this method")

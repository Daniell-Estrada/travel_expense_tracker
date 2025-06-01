import os

import requests

from src.core.interfaces import CurrencyConverter
from src.infrastructure.exceptions import ConversionError


class ApiCurrencyConverter(CurrencyConverter):
    """
    A currency converter that uses an external API to fetch exchange rates.
    This class implements the CurrencyConverter interface and provides
    functionality to convert amounts between different currencies.
    """

    def __init__(self) -> None:
        super().__init__()
        self._api_url = os.getenv("API_URL")

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Converts an amount from one currency to another using an external API.
            :param amount: The amount to convert.
            :param from_currency: The currency code of the original amount.
            :param to_currency: The currency code to convert to.
            :return: The converted amount in the target currency.
        """

        response = requests.get(
            f"{self._api_url}{from_currency.lower()}.json", timeout=10
        )

        if response.status_code != 200:
            raise ConversionError(
                f"Error fetching exchange rates: {response.status_code}"
            )

        data = response.json()
        if to_currency.lower() not in data.get(f"{from_currency.lower()}", {}):
            raise ValueError(f"Currency {to_currency} not found in exchange rates")

        conversion_rate = data[from_currency.lower()][to_currency.lower()]
        return amount * conversion_rate

from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.infrastructure.exceptions import ConversionError
from src.infrastructure.external import ApiCurrencyConverter


class TestApiCurrencyConverter(TestCase):
    """Test case for TestApiCurrencyConverter class."""

    def __init__(self, methodName: str = "runTest") -> None:
        """
        Initializes the test case with an instance of ApiCurrencyConverter.
        """

        super().__init__(methodName)
        self.converter = ApiCurrencyConverter()

    @patch("requests.get")
    def test_conversion_success(self, mock_get):
        """
        Tests the conversion of an amount from one currency to another.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"usd": {"cop": 40000}}
        mock_get.return_value = mock_response

        result = self.converter.convert(100, "USD", "COP")

        self.assertEqual(result, 4000000)

    @patch("requests.get")
    def test_conversion_error(self, mock_get):
        """
        Tests the conversion when the API returns an error status code.
        """

        mock_response = MagicMock()
        mock_response.status_code = 404
        # Simular respuesta malformada sin campo 'result'
        mock_response.json.return_value = {"error": "Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(ConversionError):
            self.converter.convert(100, "TEST", "COP")

    @patch("requests.get")
    def test_conversion_same_currency(self, mock_get):
        """
        Tests the conversion when the source and target currencies are the same.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"usd": {"usd": 1}}
        mock_get.return_value = mock_response

        result = self.converter.convert(100, "USD", "USD")

        self.assertEqual(result, 100)

    @patch("requests.get")
    def test_conversion_http_error(self, mock_get):
        """
        Tests the conversion when the API returns a 500 Internal Server Error.
        """

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_get.return_value = mock_response

        with self.assertRaises(ConversionError):
            self.converter.convert(100, "USD", "COP")
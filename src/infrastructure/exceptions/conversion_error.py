class ConversionError(Exception):
    """Exception raised for errors in the conversion process."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ConversionError: {self.message}"

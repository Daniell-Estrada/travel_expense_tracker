class InactiveTripError(Exception):
    """Exception raised when an inactive trip is encountered."""

    def __init__(
        self, message: str = "Cannot add expenses to a completed trip"
    ) -> None:
        """
        Initializes the InactiveTripError with a default message.
        """
        self.message = message
        super().__init__(self.message)

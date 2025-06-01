from enum import Enum


class PaymentMethod(Enum):
    """
    Enum representing different payment methods.
    """

    CASH = "Cash"
    CARD = "Card"

    def __str__(self):
        return self.value

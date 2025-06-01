from enum import Enum


class ExpenseType(Enum):
    """
    Enum representing different types of expenses.
    """

    TRANSPORTATION = "Transportation"
    ACCOMMODATION = "Accommodation"
    FOOD = "Food"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    OTHER = "Other"

    def __str__(self):
        return self.value

from enum import Enum

<<<<<<< HEAD

=======
>>>>>>> 0c16acf188a99d26a380ec15fd3a8fa1bc0bdf6c
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

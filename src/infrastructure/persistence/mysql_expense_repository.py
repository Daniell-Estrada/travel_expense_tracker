from datetime import date
from typing import List
from uuid import UUID

from mysql.connector import Error

from core.domain import Expense
from core.enums import ExpenseType, PaymentMethod
from core.interfaces.repositories import ExpenseRepository
from infrastructure.database import DatabaseConnection


class MySQLExpenseRepository(ExpenseRepository):
    """
    MySQL implementation of ExpenseRepository.
    Handles persistence operations for Expense entities.
    """

    def __init__(self, db_connection: DatabaseConnection) -> None:
        self._db_connection = db_connection

    def save(self, expense: Expense) -> None:
        """
        Saves an expense to the database.
            :param expense: Expense object to be saved.
            :raises RuntimeError: If there is an error during the database operation.
        """

        query = """
            INSERT INTO expenses (expense_id, trip_id, expense_date, original_amount, 
                currency, converted_amount_cop, payment_method, expense_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            with self._db_connection.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    query,
                    (
                        str(expense.expense_id),
                        str(expense.trip_id),
                        expense.expense_date,
                        expense.original_amount,
                        expense.currency,
                        expense.converted_amount_cop,
                        expense.payment_method.value,
                        expense.expense_type.value,
                    ),
                )
                connection.commit()
        except Error as e:
            raise RuntimeError(f"Error saving expense: {e}") from e

    def get_by_trip_and_date(self, trip_id: UUID, expense_date: date) -> List[Expense]:
        """
        Retrieves all expenses for a specific trip on a given date.
            :param trip_id: Unique identifier for the trip.
            :param expense_date: Date of the expenses to retrieve.
            :return: List of Expense objects for the given trip and date.
        """
        query = "SELECT * FROM expenses WHERE trip_id = %s AND expense_date = %s"

        try:
            with self._db_connection.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (str(trip_id), expense_date))
                results = cursor.fetchall()

                return [self._map_to_expense(row) for row in results]
        except Error as e:
            raise RuntimeError(f"Error retrieving expenses: {e}") from e

    def get_by_trip_id(self, trip_id: UUID) -> List[Expense]:
        """
        Retrieves all expenses for a specific trip.
            :param trip_id: Unique identifier for the trip.
            :return: List of Expense objects for the given trip_id.
        """
        query = "SELECT * FROM expenses WHERE trip_id = %s"

        try:
            with self._db_connection.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (str(trip_id),))
                results = cursor.fetchall()

                return [self._map_to_expense(row) for row in results]
        except Error as e:
            raise RuntimeError(f"Error retrieving expenses: {e}") from e

    def _map_to_expense(self, row: dict) -> Expense:
        """
        Maps a database row to an Expense object.
            :param row: Dictionary representing a row from the expenses table.
            :return: Expense object populated with data from the row.
        """
        return Expense(
            expense_id=UUID(row["expense_id"]),
            trip_id=UUID(row["trip_id"]),
            expense_date=row["expense_date"],
            original_amount=float(row["original_amount"]),
            currency=row["currency"],
            converted_amount_cop=float(row["converted_amount_cop"]),
            payment_method=PaymentMethod(row["payment_method"]),
            expense_type=ExpenseType(row["expense_type"]),
        )

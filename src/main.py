import sys

from core.services import ExpenseManager, ReportService, TripService
from infrastructure.database import DatabaseConnection
from infrastructure.external import ApiCurrencyConverter
from infrastructure.persistence import (MySQLExpenseRepository,
                                        MySQLTripRepository)
from presentation.console import ConsoleInterface


def main():
    """
    Main entry point for the application.
    """
    try:
        db_connection = DatabaseConnection()

        trip_repository = MySQLTripRepository(db_connection)
        expense_repository = MySQLExpenseRepository(db_connection)
        currency_converter = ApiCurrencyConverter()

        trip_service = TripService(trip_repository)
        expense_manager = ExpenseManager(
            expense_repository=expense_repository,
            trip_repository=trip_repository,
            currency_converter=currency_converter,
        )
        report_service = ReportService(
            expense_repository=expense_repository, trip_repository=trip_repository
        )

        console_interface = ConsoleInterface(
            trip_service=trip_service,
            expense_manager=expense_manager,
            report_service=report_service,
        )

        console_interface.run()

    except Exception as e:
        print(f"Failed to start application: {e}")
        print("Please check your database configuration in the .env file.")
        sys.exit(1)


if __name__ == "__main__":
    main()

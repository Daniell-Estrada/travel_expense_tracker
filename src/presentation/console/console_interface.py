import sys
from datetime import date, datetime
from uuid import UUID

from tabulate import tabulate

from application.dto import ExpenseDTO
from core.domain import Trip
from core.enums import ExpenseType, PaymentMethod
from core.services import ExpenseManager, ReportService, TripService


class ConsoleInterface:
    """
    Console interface for the Travel Expense Tracker application.
    Provides a command-line interface for users to manage trips and expenses.
    """

    def __init__(
        self,
        trip_service: TripService,
        expense_manager: ExpenseManager,
        report_service: ReportService,
    ) -> None:
        """
        Initializes the console interface with necessary managers.
            :param trip_service: Instance of TripService for trip operations.
            :param expense_manager: Instance of ExpenseManager for expense operations.
            :param report_service: Instance of ReportService for generating reports.
        """
        self._trip_service = trip_service
        self._expense_manager = expense_manager
        self._report_service = report_service

    def run(self) -> None:
        """Starts the console interface and displays the main menu."""
        print("=== Travel Expense Tracker ===")
        print("Welcome to your personal travel expense manager!")

        while True:
            try:
                self._show_main_menu()
                choice = input("\nSelect an option: ").strip()

                if choice == "1":
                    self._create_trip()
                elif choice == "2":
                    self._list_trips()
                elif choice == "3":
                    self._manage_trip()
                elif choice == "4":
                    self._view_reports()
                elif choice == "5":
                    print("Thank you for using Travel Expense Tracker!")
                    sys.exit(0)
                else:
                    print("Invalid option. Please try again.")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")

    def _show_main_menu(self) -> None:
        """Displays the main menu options."""
        print(f"\n{'=' * 50}")
        print("MAIN MENU")
        print("=" * 50)
        print("1. Create New Trip")
        print("2. List All Trips")
        print("3. Add Expenses to Trip")
        print("4. View Reports")
        print("5. Exit")

    def _create_trip(self) -> None:
        """Handles trip creation process."""
        print("\n--- Create New Trip ---")

        try:
            start_date = self._get_date_input("Enter start date (YYYY-MM-DD): ")
            end_date = self._get_date_input("Enter end date (YYYY-MM-DD): ")

            is_international = self._get_yes_no_input(
                "Is this an international trip? (y/n): "
            )

            currency = "COP"
            if is_international:
                currency = (
                    input("Enter currency code (e.g., USD, EUR): ").strip().upper()
                )
                if len(currency) != 3:
                    print("Invalid currency code. Using USD as default.")
                    currency = "USD"

            daily_budget = self._get_float_input("Enter daily budget in COP: ")

            trip = self._trip_service.create_trip(
                start_date=start_date,
                end_date=end_date,
                is_international=is_international,
                daily_budget=daily_budget,
                currency=currency,
            )

            print("\n✓ Trip created successfully!")
            print(f"Trip ID: {trip.trip_id}")
            print(f"Duration: {start_date} to {end_date}")
            print(f"Type: {'International' if is_international else 'Domestic'}")
            print(f"Daily Budget: {daily_budget:,.2f} COP")

        except ValueError as e:
            print(f"Error creating trip: {e}")

    def _list_trips(self) -> None:
        """Lists all trips in a tabular format."""
        print("\n--- All Trips ---")

        trips = self._trip_service.get_all_trips()

        if not trips:
            print("No trips found.")
            return

        headers = ["ID", "Start Date", "End Date", "Type", "Daily Budget", "Status"]
        rows = []

        for trip in trips:
            status = "Active" if trip.is_active() else "Completed"
            trip_type = "International" if trip.is_international else "Domestic"

            rows.append(
                [
                    str(trip.trip_id)[:8] + "...",
                    trip.start_date,
                    trip.end_date,
                    trip_type,
                    f"{trip.daily_budget:,.2f} {trip.currency}",
                    status,
                ]
            )

        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def _manage_trip(self) -> None:
        """Handles trip management (adding expenses)."""
        print("\n--- Manage Trip ---")

        trips = self._trip_service.get_all_trips()
        if not trips:
            print("No trips found. Create a trip first.")
            return

        # Show trips and let user select
        self._list_trips()

        trip_id_input = input("\nEnter trip ID (first 8 characters): ").strip()

        selected_trip = None
        for trip in trips:
            if str(trip.trip_id).startswith(trip_id_input):
                selected_trip = trip
                break

        if not selected_trip:
            print("Trip not found.")
            return

        print(
            f"\nSelected trip: {selected_trip.start_date} to {selected_trip.end_date}"
        )

        if not selected_trip.is_active():
            print("This trip has ended. Cannot add new expenses.")
            return

        self._add_expense_to_trip(selected_trip)

    def _add_expense_to_trip(self, trip: Trip) -> None:
        """Adds an expense to a specific trip."""
        print("\n--- Add Expense to Trip ---")

        try:
            expense_date = self._get_date_input("Enter expense date (YYYY-MM-DD): ")

            # Validate date is within trip period
            if expense_date < trip.start_date or expense_date > trip.end_date:
                print(
                    f"Expense date must be between {trip.start_date} and {trip.end_date}"
                )
                return

            amount = self._get_float_input(f"Enter amount in {trip.currency}: ")

            payment_method = self._get_payment_method()
            expense_type = self._get_expense_type()

            expense_dto = ExpenseDTO(
                trip_id=trip.trip_id,
                expense_date=expense_date,
                amount=amount,
                payment_method=payment_method,
                expense_type=expense_type,
            )

            daily_difference = self._expense_manager.register_expense(expense_dto)

            print("\n✓ Expense registered successfully!")
            print(f"Amount: {amount:,.2f} {trip.currency}")
            print(f"Payment Method: {payment_method.value}")
            print(f"Type: {expense_type.value}")
            print(f"Daily Budget Difference: {daily_difference:,.2f} COP")

            if daily_difference < 0:
                print("⚠️  You have exceeded your daily budget!")
            elif daily_difference == 0:
                print("✓ You have reached your daily budget exactly.")
            else:
                print("✓ You are within your daily budget.")

        except Exception as e:
            print(f"Error adding expense: {e}")

    def _view_reports(self) -> None:
        """Handles report viewing."""
        print("\n--- Reports ---")

        trips = self._trip_service.get_all_trips()
        if not trips:
            print("No trips found.")
            return

        # Show trips and let user select
        self._list_trips()

        trip_id_input = input("\nEnter trip ID (first 8 characters): ").strip()

        selected_trip = None
        for trip in trips:
            if str(trip.trip_id).startswith(trip_id_input):
                selected_trip = trip
                break

        if not selected_trip:
            print("Trip not found.")
            return

        print(
            f"\n--- Reports for Trip: {selected_trip.start_date} to {selected_trip.end_date} ---"
        )

        while True:
            print("\n1. Daily Expense Report")
            print("2. Expense Type Report")
            print("3. Trip Summary")
            print("4. Back to Main Menu")

            choice = input("\nSelect report type: ").strip()

            if choice == "1":
                self._show_daily_report(selected_trip.trip_id)
            elif choice == "2":
                self._show_type_report(selected_trip.trip_id)
            elif choice == "3":
                self._show_trip_summary(selected_trip.trip_id)
            elif choice == "4":
                break
            else:
                print("Invalid option.")

    def _show_daily_report(self, trip_id: UUID) -> None:
        """Shows daily expense report."""
        print("\n--- Daily Expense Report ---")

        daily_report = self._report_service.generate_daily_expense_report(trip_id)

        if not daily_report:
            print("No expenses found for this trip.")
            return

        headers = ["Date", "Cash (COP)", "Card (COP)", "Total (COP)"]
        rows = []

        for expense_date in sorted(daily_report.keys()):
            data = daily_report[expense_date]
            rows.append(
                [
                    expense_date,
                    f"{data['cash']:,.2f}",
                    f"{data['card']:,.2f}",
                    f"{data['total']:,.2f}",
                ]
            )

        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def _show_type_report(self, trip_id: UUID) -> None:
        """Shows expense type report."""
        print("\n--- Expense Type Report ---")

        type_report = self._report_service.generate_expense_type_report(trip_id)

        if not type_report:
            print("No expenses found for this trip.")
            return

        headers = ["Expense Type", "Cash (COP)", "Card (COP)", "Total (COP)"]
        rows = []

        for expense_type, data in type_report.items():
            rows.append(
                [
                    expense_type.value,
                    f"{data['cash']:,.2f}",
                    f"{data['card']:,.2f}",
                    f"{data['total']:,.2f}",
                ]
            )

        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def _show_trip_summary(self, trip_id: UUID) -> None:
        """Shows trip summary report."""
        print("\n--- Trip Summary ---")

        summary = self._report_service.get_trip_summary(trip_id)

        print(f"Total Expenses: {summary['total_expenses']:,.2f} COP")
        print(f"Total Budget: {summary['total_budget']:,.2f} COP")
        print(f"Remaining Budget: {summary['remaining_budget']:,.2f} COP")
        print(f"Trip Duration: {summary['trip_days']} days")
        print(f"Average Daily Expense: {summary['average_daily_expense']:,.2f} COP")

        if summary["remaining_budget"] < 0:
            print("⚠️ You have exceeded your total budget!")
        else:
            print("✓ You are within your total budget.")

    def _get_date_input(self, prompt: str) -> date:
        """Gets and validates date input from user."""
        while True:
            try:
                date_str = input(prompt).strip()
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def _get_float_input(self, prompt: str) -> float:
        """Gets and validates float input from user."""
        while True:
            try:
                value = float(input(prompt).strip())
                if value < 0:
                    print("Amount cannot be negative.")
                    continue

                return value
            except ValueError:
                print("Invalid amount. Please enter a number.")

    def _get_yes_no_input(self, prompt: str) -> bool:
        """Gets yes/no input from user."""
        while True:
            response = input(prompt).strip().lower()
            if response in ("y", "yes"):
                return True

            if response in ("n", "no"):
                return False

            print("Please enter 'y' for yes or 'n' for no.")

    def _get_payment_method(self) -> PaymentMethod:
        """Gets payment method from user."""
        print("\nPayment Methods:")
        print("1. Cash")
        print("2. Card")

        while True:
            choice = input("Select payment method (1-2): ").strip()

            if choice == "1":
                return PaymentMethod.CASH

            if choice == "2":
                return PaymentMethod.CARD

            print("Invalid choice. Please select 1 or 2.")

    def _get_expense_type(self) -> ExpenseType:
        """Gets expense type from user."""
        print("\nExpense Types:")
        expense_types = list(ExpenseType)
        for i, expense_type in enumerate(expense_types, 1):
            print(f"{i}. {expense_type.value}")

        while True:
            try:
                choice = int(
                    input(f"Select expense type (1-{len(expense_types)}): ").strip()
                )

                if 1 <= choice <= len(expense_types):
                    return expense_types[choice - 1]

                print(f"Invalid choice. Please select 1-{len(expense_types)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

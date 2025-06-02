"""
Contenedor de dependencias mejorado siguiendo principios de IoC.
"""

from functools import lru_cache
from threading import Lock

from core.services import ExpenseManager, ReportService, TripService
from infrastructure.database import DatabaseConnection
from infrastructure.external import ApiCurrencyConverter
from infrastructure.persistence import (MySQLExpenseRepository,
                                        MySQLTripRepository)


class SingletonMeta(type):
    """Metaclase para implementar el patrón Singleton."""

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DependencyContainer(metaclass=SingletonMeta):
    """Contenedor de dependencias centralizado."""

    def __init__(self):
        self._db_connection = None
        self._trip_repository = None
        self._expense_repository = None
        self._currency_converter = None

    @property
    def db_connection(self) -> DatabaseConnection:
        """Proporciona una instancia de conexión a la base de datos."""
        if self._db_connection is None:
            self._db_connection = DatabaseConnection()
        return self._db_connection

    @property
    def trip_repository(self) -> MySQLTripRepository:
        """Proporciona una instancia del repositorio de viajes."""
        if self._trip_repository is None:
            self._trip_repository = MySQLTripRepository(self.db_connection)
        return self._trip_repository

    @property
    def expense_repository(self) -> MySQLExpenseRepository:
        """Proporciona una instancia del repositorio de gastos."""
        if self._expense_repository is None:
            self._expense_repository = MySQLExpenseRepository(self.db_connection)
        return self._expense_repository

    @property
    def currency_converter(self) -> ApiCurrencyConverter:
        """Proporciona una instancia del convertidor de divisas."""
        if self._currency_converter is None:
            self._currency_converter = ApiCurrencyConverter()
        return self._currency_converter

    @lru_cache()
    def get_container(self) -> "DependencyContainer":
        """Proporciona una instancia del contenedor de dependencias."""
        return self

    def get_trip_service(self) -> TripService:
        """Inyección de dependencia para TripService."""
        return TripService(trip_repository=self.trip_repository)

    def get_expense_manager(self) -> ExpenseManager:
        """Inyección de dependencia para ExpenseManager."""
        return ExpenseManager(
            expense_repository=self.expense_repository,
            trip_repository=self.trip_repository,
            currency_converter=self.currency_converter,
        )

    def get_report_service(self) -> ReportService:
        """Inyección de dependencia para ReportService."""
        return ReportService(
            expense_repository=self.expense_repository,
            trip_repository=self.trip_repository,
        )

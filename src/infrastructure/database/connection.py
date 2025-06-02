from contextlib import contextmanager
from typing import Optional

from mysql.connector import Error, pooling

from config.settings import Settings


class DatabaseConnection:
    """
    Manages database connections following the Singleton pattern.
    Handles MySQL connection configuration and provides connection context.
    """

    _instance: Optional["DatabaseConnection"] = None
    _connection_pool = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            settings = Settings()
            self._host = settings.db_host
            self._port = settings.db_port
            self._database = settings.db_name
            self._user = settings.db_user
            self._password = settings.db_password
            self._initialized = True

    def create_connection_pool(self) -> None:
        """Creates a connection pool for database connections."""
        try:
            self._connection_pool = pooling.MySQLConnectionPool(
                pool_name="travel_expense_pool",
                pool_size=5,
                pool_reset_session=True,
                host=self._host,
                port=self._port,
                database=self._database,
                user=self._user,
                password=self._password,
                autocommit=True,
            )
        except Error as e:
            raise ConnectionError(f"Error creating connection pool: {str(e)}")

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures proper connection handling and cleanup.
        """
        if self._connection_pool is None:
            self.create_connection_pool()

        connection = None
        try:
            if not self._connection_pool:
                raise ConnectionError("Connection pool is not initialized.")

            connection = self._connection_pool.get_connection()
            yield connection
        except Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection and connection.is_connected():
                connection.close()

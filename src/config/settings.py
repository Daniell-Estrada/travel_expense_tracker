import os
from dataclasses import dataclass
from threading import Lock

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Configuration settings for the Travel Expense Tracker API.
    This class uses Pydantic for settings management and follows the Singleton pattern.
    """

    # API configuration
    API_V1_PREFIX: str = "/api/v1"
    app_name: str = "Travel Expense Tracker API"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    # Database configuration
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_name: str = os.getenv("DB_NAME", "travel_expense_tracker")
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "password")

    # External API configuration
    api_url: str = os.getenv("API_URL", "")

    # CORS configuration
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    @dataclass
    class Config:
        """Configuration for Pydantic settings."""

        env_file = ".env"
        case_sensitive = False

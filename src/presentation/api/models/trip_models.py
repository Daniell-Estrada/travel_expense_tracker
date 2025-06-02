from dataclasses import dataclass
from datetime import date
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class TripCreateRequest(BaseModel):
    """Model for creating a new Trip."""

    start_date: date = Field(..., description="Date of the start of the trip")
    end_date: date = Field(..., description="Date of the end of the trip")
    is_international: bool = Field(
        ..., description="Indicates if the trip is international"
    )
    daily_budget: float = Field(..., gt=0, description="Daily budget for the trip")
    currency: str = Field(default="COP", description="Currency for the trip budget")


class TripResponse(BaseModel):
    """Model for returning Trip details."""

    trip_id: UUID
    start_date: date
    end_date: date
    is_international: bool
    daily_budget: float
    currency: str
    is_active: bool

    @dataclass
    class Config:
        """Configuration for the TripResponse model."""

        from_attributes = True


class TripListResponse(BaseModel):
    """Model for returning a list of Trips."""

    trips: List[TripResponse]
    total: int


class TripUpdateRequest(BaseModel):
    """Model for updating an existing Trip."""

    daily_budget: float = Field(..., gt=0, description="New daily budget for the trip")
    currency: str = Field(..., description="New currency for the trip budget")

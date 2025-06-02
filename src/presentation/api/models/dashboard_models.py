from dataclasses import dataclass

from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    """Modelo de respuesta para las estadísticas del dashboard."""

    total_trips: int
    active_trips: int
    total_expenses: float
    avg_daily_expense: float

    @dataclass
    class Config:
        """Configuración para el modelo DashboardStatsResponse."""

        from_attributes = True

from .dashboard_controller import router as dashboard_router
from .expense_controller import router as expense_router
from .report_controller import router as report_router
from .trip_controller import router as trip_router

__all__ = [
    "dashboard_router",
    "expense_router",
    "report_router",
    "trip_router",
]

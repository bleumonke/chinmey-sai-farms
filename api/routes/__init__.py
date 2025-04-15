from .customers_route import router as customer_router
from .layouts_route import router as layout_router
from .plots_route import router as plots_router

__routes__ = [
    customer_router,
    layout_router,
    plots_router
]
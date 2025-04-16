from .customers import router as customer_router
from .layouts import router as layout_router
from .plots import router as plots_router
from .extent_ranges import router as extent_ranges_router
from .crops import router as crops_router
from .payment_mode import router as payment_mode_router

__routes__ = [
    customer_router,
    layout_router,
    plots_router,
    extent_ranges_router,
    crops_router,
    payment_mode_router
]
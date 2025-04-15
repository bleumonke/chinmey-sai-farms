from fastapi import FastAPI
from core import lifespan, __routes__

app = FastAPI(
    title="Chimney Farms API",
    description="API backend for managing customer records.",
    version="1.0.0",
    lifespan=lifespan
)

# Include all routes
for route in __routes__:
    app.include_router(route)

# Include a root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Chimney Farms API is running 🚜"}

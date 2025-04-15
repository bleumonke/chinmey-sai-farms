from fastapi import FastAPI
from routes import __routes__
from core import lifespan

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

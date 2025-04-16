from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import lifespan, __routes__

app = FastAPI(
    title="Chimney Farms API",
    description="API backend for managing customer records.",
    version="1.0.0",
    lifespan=lifespan
)

for route in __routes__:
    app.include_router(route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Chimney Farms API is running 🚜"}

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="This is the root endpoint of the API"
)
def read_root():
    return {"message": "Hello, World!"}
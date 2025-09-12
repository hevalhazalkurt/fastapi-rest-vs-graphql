from fastapi import FastAPI

from app.api.status import router as status_router

app = FastAPI(
    title="REST vs GraphQL Showdown",
    description="A FastAPI project created to demonstrate the differences between the REST and GraphQL paradigms.",
    version="0.1.0",
)

app.include_router(status_router, tags=["Server Status"])


@app.get("/")
async def root():
    """
    Welcome to REST vs GraphQL Showdown
    """
    return {"message": "Hello World"}

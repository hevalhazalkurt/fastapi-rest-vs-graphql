from fastapi import FastAPI

from .api import graphql_app, rest_router

app = FastAPI(
    title="REST vs GraphQL Showdown",
    description="A FastAPI project created to demonstrate the differences between the REST and GraphQL paradigms.",
    version="0.1.0",
)

app.include_router(rest_router)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """
    Welcome to REST vs GraphQL Showdown
    """
    return {"message": "Hello World"}

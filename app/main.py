from fastapi import FastAPI
from api.routers import todos

app = FastAPI(
    version='1',
    description="This is an example",
)

app.include_router(todos.router)

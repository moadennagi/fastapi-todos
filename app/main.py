from api.auth.router import router as auth_router
from api.todos.router import router as todos_router
from fastapi import FastAPI

app: FastAPI = FastAPI(
    version='1',
    description="This is an example"
)

app.include_router(todos_router)
app.include_router(auth_router)


def foo(x: int) -> int:
    return x

if __name__ == '__main__':
    foo('foo')
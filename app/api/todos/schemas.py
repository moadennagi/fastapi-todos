from pydantic import BaseModel


# input validation
class TodoBase(BaseModel):
    title: str
    completed: bool = False
    description: str | None = None

class CreateTodo(TodoBase):
    pass

class UpdateTodo(TodoBase):
    pass

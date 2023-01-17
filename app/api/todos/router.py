from typing import Union

from api.dependencies import get_session
from api.todos.models import Todo
from api.todos.schemas import TodoSchema
from api.auth.dependencies import get_current_user
from api.auth.schemas import UserSchema
from api.todos.schemas import CreateTodo, UpdateTodo
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/api/todos',
    tags=['todos',],
)

@router.get('/')
def todos(
    completed: Union[bool, None] = None,
    session: Session = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user)
) -> list[TodoSchema]:
    todos = Todo.all(session)
    if completed is not None:
        todos = filter(lambda x: x.completed == completed, todos)
    todos = list(todos)
    return todos

@router.get('/{todo_id}')
def todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user)
) -> TodoSchema:
    todos = Todo.get(todo_id, session=session)
    if todos:
        todo = todos[0]
        response = todo
    else:
        raise HTTPException(status_code=404)
    return response

@router.post('/')
def create(
    todo_data: CreateTodo,
    session: Session = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user)
) -> TodoSchema:
    data = dict(todo_data)
    todo = Todo(**data)
    todo.save(session)
    todo_schema.from_orm(todo)
    return todo

@router.put('/{todo_id}')
def update(
    todo_id: int,
    todo_data: UpdateTodo,
    session: Session = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user)
) -> TodoSchema:
    todo = Todo.get(todo_id, session)
    if not todo:
        raise HTTPException(status_code=404)
    todo = todo[0]
    res = Todo.update(todo_id, dict(todo_data), session=session)
    return res

@router.delete('/{todo_id}')
def delete(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user)
) -> TodoSchema:
    todo = Todo.get(todo_id, session)
    if not todo:
        raise HTTPException(404)
    res = todo.delete()
    return res

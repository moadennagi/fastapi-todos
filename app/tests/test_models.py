# test CRUDMixin
import pytest

from sqlalchemy import select, delete
from api.models import Todo, CreateTodo


@pytest.fixture
def todo(session):
    todo = Todo(title='foo')
    session.add(todo)
    session.flush()
    yield todo
    session.delete(todo)
    session.commit()

@pytest.fixture
def todos(session):
    todos = []
    for i in range(5):
        todos.append(Todo(title=f'foo-{i}'))
    session.add_all(todos)
    session.flush()
    yield todos
    # delete all created todos
    pks = [todo.id for todo in todos]
    q = delete(Todo).where(Todo.id.in_(pks))
    session.execute(q)
    session.commit()

def test_get_should_return_one_result(todo, session):
    res = Todo.get(todo.id, session=session)
    assert res.title == todo.title

def test_get_should_raise_not_found(session):
    pass

def test_create_should_return_instance(todo, session):
    data = CreateTodo(title='bar')
    todo = Todo.create(data, session)
    assert todo.id

def test_update_should_return_updated_instance(todo, session):
    data = {'title': 'modified'}
    todo = Todo.update(todo.id, data, session)
    assert todo.title == data['title']

def test_bulk_delete_should_delete_all_given_ids(session, todos):
    pks = [todo.id for todo in todos]
    Todo.bulk_delete(pks, session)

    q = select(Todo).where(Todo.id.in_(pks))
    res = session.execute(q).fetchall()
    assert not res
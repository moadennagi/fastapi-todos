""
import pytest
from api.todos.models import Todo
from sqlalchemy.orm import Session


@pytest.fixture
def tasks(session: Session):
    data = [{'title': f'task-{i}', 'completed': False} for i in range(5)]
    for i, obj in enumerate(data):
        if i == 1:
            obj['completed'] = True
        session.add(Todo(**obj))
    session.flush()
    yield Todo.all(session)

def test_get_tasks_should_return_unauthorized(tasks, client):
    response = client.get('/api/todos/')
    assert response.status_code == 401

def test_get_one_task_by_id(tasks):
    ...

def test_raise_not_found(tasks):
    ...

def test_filter_completed_tasks(tasks):
    ...

def test_create_a_task(client):
    response = client.post('/api/todos/', json={})
    assert response.status_code == 401

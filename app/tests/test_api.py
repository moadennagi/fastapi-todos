""
import pytest

from sqlalchemy.orm import Session
from api.models import Todo

@pytest.fixture
def tasks(session: Session):
    data = [{'title': f'task-{i}', 'completed': False} for i in range(5)]
    for i, obj in enumerate(data):
        if i == 1:
            obj['completed'] = True
        session.add(Todo(**obj))
    session.flush()
    yield Todo.all(session)

def test_get_tasks(tasks, client):
    response = client.get('/api/v1/todos')
    print(response.json())

def test_get_one_task_by_id(tasks):
    ...

def test_raise_not_found(tasks):
    ...

def test_filter_completed_tasks(tasks):
    ...

def test_create_a_task(tasks):
    ...
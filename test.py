import pytest
from main import app
import database

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_db():
    database.init_db()
    with database.get_db_connection() as conn:
        conn.execute("DELETE FROM tasks")
        conn.commit()

def test_get_all_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json == []

def test_create_task(client):
    response = client.post("/task", data={"title": "Test Task", "description": "Description"})
    assert response.status_code == 302

    response = client.get("/tasks")
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Test Task"

def test_toggle_task(client):
    client.post("/task", data={"title": "Toggle Task", "description": "Test"})
    tasks = client.get("/tasks").json
    task_id = tasks[0]['id']

    task = client.get(f"/task/{task_id}").json
    assert task.get('done', 0) == 0

    response = client.post(f"/task/{task_id}/toggle")
    assert response.status_code == 302

    task = client.get(f"/task/{task_id}").json
    assert task.get('done', 1) == 1

def test_delete_task(client):
    client.post("/task", data={"title": "To Delete", "description": "Test"})
    
    task_id = client.get("/tasks").json[0]['id']

    response = client.delete(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"
    
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 404
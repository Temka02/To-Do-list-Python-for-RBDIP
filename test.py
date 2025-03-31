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
    
    response = client.post("/task/1/toggle")
    assert response.status_code == 302  

    response = client.get("/task/1")
    assert response.json["done"] == 1

def test_delete_task(client):
    client.post("/task", data={"title": "To Delete", "description": "Test"})
    
    response = client.delete("/task/1")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"

    response = client.get("/task/1")
    assert response.status_code == 404
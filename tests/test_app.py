from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_calculate():
    response = client.post("/calculate/", json={"x": 5, "y": 3, "operator": "+"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_result():
    task_id = "some_task_id"
    response = client.get(f"/result/?task_id={task_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "status" in response.json()
    assert "result" in response.json()


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for task in response.json():
        assert "id" in task
        assert "status" in task
        assert "result" in task


def test_get_result_with_real_task_id():

    response = client.post("/calculate/", json={"x": 5, "y": 3, "operator": "+"})
    assert response.status_code == 200
    task_id = response.json()["id"]

    response = client.get(f"/result/?task_id={task_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "status" in response.json()
    assert "result" in response.json()

    assert response.json()["id"] == task_id
    assert response.json()["result"] == '8'

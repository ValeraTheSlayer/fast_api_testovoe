from fastapi import FastAPI
import uuid

from app.models import TaskStatus, CalcTask
from app.tasks import async_calculate

app = FastAPI()

tasks = {}


@app.post("/calculate/", response_model=TaskStatus)
async def calculate(task: CalcTask):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "task": task, "result": None}
    return TaskStatus(id=task_id, status="pending", result="Not calculated yet")


@app.get("/result/", response_model=TaskStatus)
async def get_result(task_id: str):
    task_data = tasks.get(task_id, {"status": "not_found", "result": None})

    if task_data["status"] == "not_found":
        return TaskStatus(id=task_id, status="not_found", result="Not found")

    if task_data["status"] == "pending":
        try:
            task = task_data["task"]
            result = await async_calculate(task.x, task.y, task.operator)
            task_data["status"] = "complete"
            task_data["result"] = result
        except Exception as e:
            task_data["status"] = "error"
            task_data["result"] = str(e)

    return TaskStatus(id=task_id, status=task_data["status"], result=str(task_data["result"]))


@app.get("/tasks/", response_model=list[TaskStatus])
def get_tasks():
    return [TaskStatus(id=task_id, status=task["status"], result=str(task["result"])) for task_id, task in
            tasks.items()]

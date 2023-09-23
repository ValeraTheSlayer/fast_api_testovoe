import logging.config
import uuid

import uvicorn
from fastapi import FastAPI

from models import TaskStatus, CalcTask
from tasks import async_calculate

from logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()

tasks = {}


@app.post("/calculate/", response_model=TaskStatus)
async def calculate(task: CalcTask):
    logger.info(f"Получено расчетное задание: {task.model_dump()}")
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "task": task, "result": None}
    logger.debug(f"Создана новая задача с идентификатором: {task_id}")
    return TaskStatus(id=task_id, status="pending", result="Not calculated yet")


@app.get("/result/", response_model=TaskStatus)
async def get_result(task_id: str):
    logger.info(f"Получение результата для идентификатора задачи: {task_id}")
    task_data = tasks.get(task_id, {"status": "not_found", "result": None})

    if task_data["status"] == "not_found":
        logger.warning(f"Зада с идентификатором {task_id} не найдена")
        return TaskStatus(id=task_id, status="not_found", result="Not found")

    if task_data["status"] == "pending":
        try:
            task = task_data["task"]
            result = await async_calculate(task.x, task.y, task.operator)
            task_data["status"] = "complete"
            task_data["result"] = result
            logger.debug(f"Задача {task_id} завершена со следующим результатом: {result}")
        except Exception as e:
            task_data["status"] = "error"
            task_data["result"] = str(e)
            logger.error(f"При обработки задачи произошла ошибка {task_id}: {str(e)}")

    return TaskStatus(id=task_id, status=task_data["status"], result=str(task_data["result"]))


@app.get("/tasks/", response_model=list[TaskStatus])
def get_tasks():
    logger.info("Выборка всех задач")
    return [TaskStatus(id=task_id, status=task["status"], result=str(task["result"])) for task_id, task in
            tasks.items()]


if __name__ == '__main__':
    uvicorn.run("api:app", host='127.0.0.1', port=8000, reload=True, workers=3)

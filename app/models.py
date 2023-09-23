from pydantic import BaseModel

class CalcTask(BaseModel):
    x: int
    y: int
    operator: str

class TaskStatus(BaseModel):
    id: str
    status: str
    result: str

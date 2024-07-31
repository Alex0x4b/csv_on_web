from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
tasks = []


class Task(BaseModel):
    # Ensure input is correct to avoid DB injection or unespected behaviour
    id: Optional[int] = None  # Handle by data base
    task: str
    is_completed: bool = False


@app.get("/get_tasks")
async def get_tasks():
    return tasks


@app.get("/get_tasks/{id}")
async def get_task_by_id(id: int):
    task = [task for task in tasks if task.id == id][0]
    return task


@app.post("/add_task")
async def add_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task

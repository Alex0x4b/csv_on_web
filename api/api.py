from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
tasks = []


class BaseTask(BaseModel):
    # Ensure input is correct to avoid DB injection or unespected behaviour
    task: str


class Task(BaseTask):
    id: Optional[int] = None  # Handle by data base
    is_completed: bool = False


class ReturnTask(BaseTask):
    pass


@app.post("/add_task", response_model=ReturnTask)
async def add_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task


@app.put("/update_task/{id}")
async def update_task(id: int, modified_task: Task):
    for index, task in enumerate(tasks):
        if task.id == id:
            tasks[index] = modified_task
            tasks[index].id = id
    return


@app.delete("/delete_task/{id}")
async def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task.id == id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail="item id not found")


@app.get("/get_tasks")
async def get_tasks(completed: Optional[bool] = None):
    if completed is not None:
        return [task for task in tasks if task.is_completed == completed]
    return tasks


@app.get("/get_tasks/{id}")
async def get_task_by_id(id: int):
    for task in tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="item id not found")

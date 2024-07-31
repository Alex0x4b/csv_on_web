from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from time import time


app = FastAPI()
tasks = []


class BaseTask(BaseModel):
    # Ensure input is correct to avoid DB injection or unespected behaviour
    task: str


class Task(BaseTask):
    # A task is BaseTask + Task attributes
    id: Optional[int] = None  # Handle by data base
    is_completed: bool = False


class ReturnTask(BaseTask):
    # Returning BaseTask
    pass


# Default middleware build by fast api
# CORSMiddleware improve security by restrict who can query the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # from everywhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Custom middleware to execute code before and after the route
@app.middleware("http")
async def log_proceess_time_middleware(request, call_next):
    # Before the root
    start_time = time()
    # The route
    response = await call_next(request)
    # After the route
    end_time = time()
    process_time = end_time - start_time
    print(f"Request {request.url} processed in {process_time} seconds")
    return response


@app.post("/add_task", response_model=ReturnTask)  # possible to mock a response model
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
async def get_tasks(completed: Optional[bool] = None):  # add parameters
    if completed is not None:
        return [task for task in tasks if task.is_completed == completed]
    return tasks


@app.get("/get_tasks/{id}")
async def get_task_by_id(id: int):
    for task in tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="item id not found")

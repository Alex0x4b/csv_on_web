from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
import asyncio
from time import time, sleep


app = FastAPI()
templates = Jinja2Templates(directory="web/templates")

tasks = []


"""
Type Classe
===========
"""


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


"""
Middleware
==========
"""


# Default middleware build by fastapi
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


async def send_email(task: Task):
    print(f"Start sending email for {task.id}...")
    await asyncio.sleep(3)
    print(f"OK: email notification form task {task.id} sent")


"""
Endpoints
=========
"""


@app.get("/", response_class=HTMLResponse)
def get_homepage(request: Request):
    context = {"total_tasks": len(tasks)}
    return templates.TemplateResponse(
        request=request, name="index.html", context=context)


# it is possible to mock a response model (i.e. filter object for response)
# it is possible to send task in the background and returning right away to not block
# the API. Note: the BackgroundTask will inot be returning by the API even when finished
@app.post("/add_task", response_model=ReturnTask)
async def add_task(task: Task, background_task: BackgroundTasks):
    task.id = len(tasks) + 1
    tasks.append(task)
    background_task.add_task(send_email, task=task)
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
async def get_tasks(
    id: int | None = None,
    completed: bool | None = None
):
    filtered_tasks = tasks.copy()
    if id is not None:
        filtered_tasks = [task for task in filtered_tasks if task.id == id]
    if completed is not None:
        filtered_tasks = [
            task for task in filtered_tasks
            if task.is_completed == completed
        ]
    return filtered_tasks

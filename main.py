from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Изучить FastAPI"},
    {"id": 2, "title": "Настроить GitLab"},
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None

@app.get("/")
def home():
    return {"message": "Hello, ToDo!"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": max((item["id"] for item in tasks), default=0) + 1,
        "title": task.title
    }

    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: int,task: TaskUpdate):
    for existing_task in tasks:
        if existing_task["id"] == task_id:
            if task.title is not None:
                existing_task["title"] = task.title
            return existing_task
    raise HTTPException(
        status_code=404,
        detail="Задача не найдена"
    )

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            deleted_task = tasks.pop(index)

            return {
                "message": "Задача удалена",
                "task": deleted_task    
            }
    raise HTTPException(
        status_code=404,
        detail="Задача не найдена"
    )
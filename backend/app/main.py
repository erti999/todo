from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, ToDo!"}

@app.get("/tasks")
def get_tasks(db: Annotated[Session, Depends(get_db)]):
    statement = select(Task)
    tasks = db.scalars(statement).all()
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, db: Annotated[Session, Depends(get_db)]):
    new_task = Task(title=task.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: int,task: TaskUpdate, db: Annotated[Session, Depends(get_db)]):
    db_task = db.get(Task, task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена"
        )
    changes = task.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    db_task = db.get(Task, task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена"
        )
    db.delete(db_task)
    db.commit()
    return {"message": "Задача удалена"}
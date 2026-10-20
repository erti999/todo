from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import task_service
from app.schemas import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])
DBSession = Annotated[Session, Depends(get_db)]

@router.get("")
def get_tasks(db: DBSession):
    return task_service.get_tasks(db)

@router.post("", status_code=201)
def create_task(task: TaskCreate, db: DBSession):
    return task_service.create_task(db, task)

@router.patch("/{task_id}")
def update_tasks(task_id: int, task: TaskUpdate, db: DBSession):
    result = task_service.update_task(db, task_id, task)
    if result is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    return result

@router.delete("/{task_id}")
def get_tasks(task_id: int, db: DBSession):
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}
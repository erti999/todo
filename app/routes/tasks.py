from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.services.task_service import TaskService
from app.schemas import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])
DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@router.get("")
async def get_tasks(db: DBSession):
    return await TaskService.get_all(db)

@router.post("", status_code=201)
async def create_task(task: TaskCreate, db: DBSession):
    return await TaskService.create(db, task)

@router.patch("/{task_id}")
async def update_tasks(task_id: int, task: TaskUpdate, db: DBSession):
    result = await TaskService.update(db, task_id, task)
    if result is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    return result

@router.delete("/{task_id}")
async def get_tasks(task_id: int, db: DBSession):
    deleted = await TaskService.delete(db, task_id)
    if not deleted:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}
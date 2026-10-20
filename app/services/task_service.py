from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.scalars(select(Task))
        return result.all()

    @staticmethod
    async def create(db: AsyncSession, schema: TaskCreate):
        task = Task(title=schema.title, completed=False)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task
 
    @staticmethod
    async def update(db: AsyncSession, task_id: int, schema: TaskUpdate):
        task = await db.get(Task, task_id)
        if task is None:
            return None
        changes = schema.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(task, field, value)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete(db: AsyncSession, task_id: int):
        task = await db.get(Task, task_id)
        if task is None:
            return None
        await db.delete(task)
        await db.commit()
        return True
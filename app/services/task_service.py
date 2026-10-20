from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

def get_tasks(db: Session):
    statement = select(Task)
    return db.scalars(statement).all()

def create_task(db: Session, task: TaskCreate):
    new_task = Task(title=task.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db:Session, task_id: int,task: TaskUpdate):
    db_task = db.get(Task, task_id)
    if db_task is None:
        return None
    changes = task.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db:Session, task_id: int):
    db_task = db.get(Task, task_id)
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return {"message": "Задача удалена"}
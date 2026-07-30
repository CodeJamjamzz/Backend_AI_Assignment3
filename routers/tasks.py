from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models import Task, TaskCreate, TaskUpdate
import database

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", summary="List tasks", response_model=List[Task])
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    result = database.tasks_db
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result

@router.get("/{task_id}", summary="Get a specific task", response_model=Task)
def get_task(task_id: int):
    for t in database.tasks_db:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.post("", summary="Create a new task", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task: TaskCreate):
    new_task = {
        "id": database.next_id,
        "title": task.title,
        "done": task.done
    }
    database.next_id += 1
    database.tasks_db.append(new_task)
    return new_task

@router.put("/{task_id}", summary="Update a task", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    for t in database.tasks_db:
        if t["id"] == task_id:
            t["title"] = task.title
            t["done"] = task.done
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.delete("/{task_id}", summary="Delete a task", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for i, t in enumerate(database.tasks_db):
        if t["id"] == task_id:
            database.tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

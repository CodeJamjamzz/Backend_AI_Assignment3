from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models import Task, TaskCreate, TaskUpdate
import database

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", summary="List tasks", response_model=List[Task])
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks"
    conditions = []
    params = []
    
    if done is not None:
        conditions.append("done = ?")
        params.append(1 if done else 0)
    if search:
        conditions.append("title LIKE ?")
        params.append(f"%{search}%")
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@router.get("/{task_id}", summary="Get a specific task", response_model=Task)
def get_task(task_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return dict(row)

@router.post("", summary="Create a new task", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task: TaskCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", 
        (task.title, 1 if task.done else 0)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": new_id,
        "title": task.title,
        "done": task.done
    }

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

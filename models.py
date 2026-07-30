from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool = False

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool

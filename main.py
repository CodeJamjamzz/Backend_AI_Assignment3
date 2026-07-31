from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import tasks
import database
import redis

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    
    # Ping Redis on startup
    try:
        r = redis.Redis(host='redis', port=6379, decode_responses=True)
        r.ping()
        print("Successfully connected to Redis and pinged!")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        
    yield

app = FastAPI(
    title="Task API",
    description="A simple PostgreSQL CRUD API for tasks. Data survives server restart.",
    version="1.0",
    lifespan=lifespan
)

# Exception handlers to match exact JSON requirements ("error" instead of "detail", 400 instead of 422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body. Title is required and cannot be empty."}
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# Include the tasks router
app.include_router(tasks.router)

@app.get("/", summary="Root endpoint - Get API information", tags=["System"])
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check endpoint", tags=["System"])
def health():
    return {"status": "ok"}

@app.get("/stats", summary="Get task statistics", tags=["System"])
def get_stats():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = TRUE")
    done_count = cursor.fetchone()['count']
    conn.close()
    
    open_count = total - done_count
    return {"total": total, "done": done_count, "open": open_count}

@app.post("/reset", summary="Reset tasks to initial state (Seed)", tags=["System"])
def reset_tasks():
    database.reset_db()
    return {"message": "Tasks reset to initial state"}

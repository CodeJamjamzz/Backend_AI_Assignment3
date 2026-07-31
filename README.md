# Task API (Assignment 2)

This is the third assignment (A3).

**Run command (Stage 0):**
`docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres`

This is a simple CRUD API for managing a to-do list, built with **Python and FastAPI**. It has been upgraded for Assignment A2 to use **SQLite** instead of in-memory storage, meaning data now persists across server restarts!

## Why SQLite?
SQLite was chosen because it's a single file database that requires zero setup (no separate database server needed). It automatically creates the file if it doesn't exist, and most importantly, it allows the data to survive restarts.

## Database Location
The database lives in a file named `tasks.db` in the root of the project. This file is created automatically when the application starts for the first time.

## Getting Started

Follow these steps to run the API locally:

1. **Install Dependencies:**
   Make sure you have Python 3.10+ installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server:**
   Start the FastAPI development server:
   ```bash
   fastapi dev main.py
   ```
   The server will start on `http://localhost:8000`. The database `tasks.db` will be created automatically and seeded with 3 default tasks.

3. **View the Swagger UI:**
   Open your browser and navigate to `http://localhost:8000/docs` to see the interactive Swagger UI and test the endpoints!

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns API information. |
| `GET` | `/health` | Health check endpoint. |
| `GET` | `/tasks` | Lists all tasks. Supports `?done=true` and `?search=term` queries. |
| `GET` | `/tasks/{id}` | Gets a specific task by ID. |
| `POST` | `/tasks` | Creates a new task. (Body requires `title`). |
| `PUT` | `/tasks/{id}` | Updates a task's title and status. |
| `DELETE` | `/tasks/{id}` | Deletes a task. |
| `GET` | `/stats` | Returns count of total, open, and completed tasks. |
| `POST` | `/reset` | Drops and recreates the SQLite table, seeding initial data. |

## Stage 4: Explored SQLite

Here is an example query I ran in DB Browser for SQLite:
```sql
SELECT * FROM tasks WHERE done = 1;
```
*Result: It returned only the tasks that were marked as completed.*

<img width="1912" height="1078" alt="image" src="https://github.com/user-attachments/assets/f130b64e-bdf1-46d5-9ac2-1f14ed74460a" />

## AI vs Me (Stage 6)

**Prompt used:**
"Please migrate this FastAPI in-memory CRUD app to use SQLite. Use `sqlite3`. Ensure the `tasks` table is created automatically if missing with columns `id INTEGER PRIMARY KEY, title TEXT, done BOOLEAN`. Seed three tasks only when the table is empty. Keep all five endpoints (`GET /tasks`, `GET /tasks/{id}`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`) identical in behavior. Use parameterized queries for all operations and preserve the `400`/`404` error rules."

**Differences found:**
1. **Transaction Handling:** The AI used explicit transactions gracefully by relying on `conn.commit()` wrapped around `try-except` blocks to handle rollback on errors, whereas my hand-rolled version was a bit more simplistic.
2. **Type conversions:** The AI explicitly ensured the `done` boolean value from FastAPI was cast as `1` or `0` for SQLite insertions properly, preventing subtle bugs that arise from Boolean conversions in older Python versions.
3. **Response dictionaries:** The AI used `sqlite3.Row` and dictated `dict(row)` explicitly across the board to serialize database rows into JSON automatically, something I only learned after trial and error.

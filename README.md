# Task API (Assignment 1)

This is a simple, in-memory CRUD API for managing a to-do list, built with **Python and FastAPI**. It was built for Assignment A1.

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
   The server will start on `http://localhost:8000`.

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
| `POST` | `/reset` | Resets the in-memory tasks list back to the initial 3 examples. |

## Why data disappears on restart
If you create a task and then restart the server, the new task will be gone. This happens because the tasks are stored in a simple Python list in the program's memory. When the program stops, the memory is cleared. To make the data survive restarts, it would need to be saved to a database (which is what Week 3 is for!).

---

*(Note: Add your own screenshot of Swagger UI and example `curl -i` output here before submitting!)*

# Task API (Assignment 3)

This is a CRUD API for managing a to-do list, containerized using Docker and backed by a PostgreSQL database.

## Quick Start

1. Copy the example environment variables:
   ```bash
   cp .env.example .env
   ```

2. Start the entire stack (app + database) with one command:
   ```bash
   docker compose up -d
   ```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns API information. |
| `GET` | `/health` | Health check endpoint. |
| `GET` | `/tasks` | Lists all tasks. |
| `GET` | `/tasks/{id}` | Gets a specific task by ID. |
| `POST` | `/tasks` | Creates a new task. |
| `PUT` | `/tasks/{id}` | Updates a task's title and status. |
| `DELETE` | `/tasks/{id}` | Deletes a task. |

## Example Request

```bash
curl -i http://localhost:3000/tasks
```
```http
HTTP/1.1 200 OK
content-length: 154
content-type: application/json
date: Fri, 31 Jul 2026 13:42:00 GMT
server: uvicorn

[{"id":1,"title":"Buy groceries","done":false},{"id":2,"title":"Clean the house","done":true},{"id":3,"title":"Finish Assignment 2","done":false}]
```

## Database Screenshot

<img width="1403" height="608" alt="Screenshot 2026-07-31 235420" src="https://github.com/user-attachments/assets/a3f4e052-a692-4fcf-9ba3-40e12d4a2f44" />


## AI vs Me (Stage 6)

**Prompt used:**
"Please containerize this task CRUD API onto Postgres. We are using Python with psycopg. Ensure the `tasks` table is created automatically if missing with columns `id SERIAL PRIMARY KEY, title TEXT, done BOOLEAN`. Seed three tasks only when the table is empty. Keep all five endpoints (`GET /tasks`, `GET /tasks/{id}`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`) keeping identical behaviour, parameterized queries (`%s`). Ensure the password comes from `.env` (never hardcoded), configure a volume for persistence, and set up one-command startup with docker compose."

**Differences found:**
1. **Healthcheck:** The AI included a robust `healthcheck` in `compose.yaml` for the Postgres container, ensuring the API waits using `depends_on: db: condition: service_healthy`.
2. **Depends On:** My manual `depends_on: [db]` is valid but simplistic, whereas the AI explicitly structured it as a dictionary.
3. **Slim Image:** The AI used a multi-stage build in the Dockerfile which made the final image significantly smaller, while I used a simple single-stage `python:3.10-slim`.
4. **Ignored Parameter:** My prompt forgot to specify the port mapping for the API, but the AI correctly inferred `3000:3000` from the context of web apps.

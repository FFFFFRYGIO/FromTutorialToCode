# FastAPI Feature Showcase

A small task REST API built with [FastAPI](https://fastapi.tiangolo.com/),
a modern, high-performance Python web framework for building APIs.

## What it shows

- **Pydantic models** — automatic request/response validation & serialization
- **Automatic docs** — interactive Swagger UI at `/docs` and ReDoc at `/redoc`
- **Path & query parameters** — `/tasks/{task_id}`, filtering, pagination
- **Request bodies** — typed `POST`/`PATCH` payloads
- **Status codes & errors** — `201 Created`, `204 No Content`, `HTTPException`
- **Dependency injection** — a reusable pagination dependency
- **Type hints everywhere** — they drive validation, docs, and autocompletion

## Setup

```bash
cd fastapi_app
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Then open the interactive docs at **http://127.0.0.1:8000/docs** — you can try
every endpoint directly from the browser.

## Try the API

```bash
# List tasks
curl http://127.0.0.1:8000/tasks

# Filter by priority + paginate
curl "http://127.0.0.1:8000/tasks?priority=high&limit=10"

# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Ship the API\", \"priority\": \"high\"}"

# Update a task
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"done\": true}"

# Delete a task
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

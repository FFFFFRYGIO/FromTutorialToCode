"""
FastAPI Feature Showcase
========================

A small "tasks" REST API that demonstrates the core features of FastAPI:

- Pydantic models for request/response validation and serialization
- Automatic interactive docs (Swagger UI at /docs, ReDoc at /redoc)
- Path parameters, query parameters, and request bodies
- Proper HTTP status codes and HTTPException error handling
- Dependency injection (a simple pagination dependency)
- Type hints drive validation, docs, and editor autocompletion

Run it with:
    uvicorn main:app --reload

Then open:
    http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from itertools import count
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Task Service",
    description="A tiny task API showcasing FastAPI's main features.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class Priority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(..., min_length=1, max_length=120, examples=["Write docs"])
    priority: Priority = Priority.medium
    done: bool = False


class TaskUpdate(BaseModel):
    """Partial update — every field is optional."""

    title: str | None = Field(default=None, min_length=1, max_length=120)
    priority: Priority | None = None
    done: bool | None = None


class Task(TaskCreate):
    """Full task as returned by the API."""

    id: int
    created_at: datetime


# ---------------------------------------------------------------------------
# In-memory store (swap for a real database in production).
# ---------------------------------------------------------------------------
_id_counter = count(1)
TASKS: dict[int, Task] = {}


def _seed() -> None:
    for title, prio in [
        ("Learn FastAPI", Priority.high),
        ("Read the docs", Priority.low),
    ]:
        tid = next(_id_counter)
        TASKS[tid] = Task(
            id=tid, title=title, priority=prio, done=False, created_at=datetime.now()
        )


_seed()


# ---------------------------------------------------------------------------
# Dependency injection: reusable pagination parameters.
# ---------------------------------------------------------------------------
class Pagination(BaseModel):
    skip: int = 0
    limit: int = 50


def pagination_params(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Pagination:
    return Pagination(skip=skip, limit=limit)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["meta"])
def root():
    """Health check / welcome route."""
    return {"message": "FastAPI Task Service. Visit /docs for interactive API docs."}


@app.get("/tasks", response_model=list[Task], tags=["tasks"])
def list_tasks(
    page: Annotated[Pagination, Depends(pagination_params)],
    done: bool | None = None,
    priority: Priority | None = None,
):
    """List tasks with optional filtering and pagination."""
    items = sorted(TASKS.values(), key=lambda t: t.id)
    if done is not None:
        items = [t for t in items if t.done == done]
    if priority is not None:
        items = [t for t in items if t.priority == priority]
    return items[page.skip : page.skip + page.limit]


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate):
    """Create a new task."""
    tid = next(_id_counter)
    task = Task(id=tid, created_at=datetime.now(), **payload.model_dump())
    TASKS[tid] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: int):
    """Fetch a single task by id."""
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate):
    """Partially update an existing task."""
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    updated = task.model_copy(update=payload.model_dump(exclude_unset=True))
    TASKS[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int):
    """Delete a task."""
    if TASKS.pop(task_id, None) is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return None

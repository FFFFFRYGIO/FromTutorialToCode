"""
Flask Feature Showcase
======================

A small task-manager web app that demonstrates the core features of Flask:

- URL routing with dynamic parameters (`<int:task_id>`)
- Jinja2 templates with template inheritance (see templates/base.html)
- Serving static files (see static/style.css)
- Handling GET and POST form submissions
- Flash messages for user feedback
- A JSON REST API (GET/POST/DELETE) alongside the HTML views
- Custom error handling (404)

Run it with:
    flask --app app run --debug
or:
    python app.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from itertools import count

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

app = Flask(__name__)
# In a real app, load this from an environment variable / config file.
app.secret_key = "dev-secret-change-me"


# ---------------------------------------------------------------------------
# In-memory "database". For a real app you'd use SQLAlchemy + a real database.
# ---------------------------------------------------------------------------
@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )


_id_counter = count(1)
TASKS: dict[int, Task] = {}


def _add_task(title: str) -> Task:
    task = Task(id=next(_id_counter), title=title.strip())
    TASKS[task.id] = task
    return task


# Seed a couple of tasks so the app isn't empty on first load.
_add_task("Learn Flask routing")
_add_task("Build a JSON API")


# ---------------------------------------------------------------------------
# HTML views
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    tasks = sorted(TASKS.values(), key=lambda t: t.id)
    remaining = sum(1 for t in tasks if not t.done)
    return render_template("index.html", tasks=tasks, remaining=remaining)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Task title cannot be empty.", "error")
    else:
        _add_task(title)
        flash(f"Added task: {title}", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id: int):
    task = TASKS.get(task_id)
    if task is None:
        abort(404)
    task.done = not task.done
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id: int):
    if TASKS.pop(task_id, None) is None:
        abort(404)
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


# ---------------------------------------------------------------------------
# JSON REST API
# ---------------------------------------------------------------------------
@app.get("/api/tasks")
def api_list():
    return jsonify([asdict(t) for t in sorted(TASKS.values(), key=lambda t: t.id)])


@app.post("/api/tasks")
def api_create():
    payload = request.get_json(silent=True) or {}
    title = str(payload.get("title", "")).strip()
    if not title:
        return jsonify(error="'title' is required"), 400
    task = _add_task(title)
    return jsonify(asdict(task)), 201


@app.get("/api/tasks/<int:task_id>")
def api_get(task_id: int):
    task = TASKS.get(task_id)
    if task is None:
        return jsonify(error="not found"), 404
    return jsonify(asdict(task))


@app.delete("/api/tasks/<int:task_id>")
def api_delete(task_id: int):
    if TASKS.pop(task_id, None) is None:
        return jsonify(error="not found"), 404
    return "", 204


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_err):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

# Flask Feature Showcase

A small task-manager web app built with [Flask](https://flask.palletsprojects.com/),
a lightweight Python web framework. It serves both HTML pages and a JSON REST API.

## What it shows

- **Routing** — static and dynamic routes (`/toggle/<int:task_id>`)
- **Templates** — Jinja2 with template inheritance (`templates/base.html`)
- **Static files** — CSS served from `static/style.css`
- **Forms** — handling `GET`/`POST`, reading `request.form`
- **Flash messages** — user feedback via `flash()` / `get_flashed_messages()`
- **JSON REST API** — `GET`/`POST`/`DELETE` under `/api/tasks`
- **Error handling** — a custom 404 page

## Project structure

```
flask_app/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── about.html
    └── 404.html
```

## Setup

```bash
cd flask_app
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
flask --app app run --debug
# or
python app.py
```

Then open http://localhost:5000.

## Try the API

```bash
# List tasks
curl http://localhost:5000/api/tasks

# Create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Learn the Flask API\"}"

# Delete a task
curl -X DELETE http://localhost:5000/api/tasks/1
```

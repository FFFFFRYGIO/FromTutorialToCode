# Django Feature Showcase

A task-manager web app built with [Django](https://www.djangoproject.com/),
a "batteries-included" Python web framework. This demo highlights the parts of
Django you reach for in almost every project.

## What it shows

- **Models & ORM** — a `Task` model with choices, ordering, and a SQLite DB
- **Migrations** — schema managed via `makemigrations` / `migrate`
- **Admin site** — a fully featured CRUD admin auto-generated from the model
- **URL routing** — project- and app-level `urls.py` with named routes
- **Views** — a class-based `ListView` plus function views
- **Forms** — a `ModelForm` for validated task creation
- **Templates** — template inheritance, `{% url %}`, CSRF protection, messages framework

## Project structure

```
django_app/
├── manage.py
├── requirements.txt
├── mysite/            # project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tasks/             # the "tasks" app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── migrations/
    └── templates/tasks/
        ├── base.html
        └── task_list.html
```

## Setup

```bash
cd django_app
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

## Initialize the database

```bash
python manage.py makemigrations
python manage.py migrate
```

## (Optional) create an admin user

```bash
python manage.py createsuperuser
```

## Run

```bash
python manage.py runserver
```

Then open:

- The app: http://127.0.0.1:8000/
- The admin: http://127.0.0.1:8000/admin/ (log in with your superuser)

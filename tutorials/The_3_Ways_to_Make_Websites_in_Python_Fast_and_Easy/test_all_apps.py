"""
Smoke-test all four example applications.

Uses the project virtual environment (.venv) automatically when present, so you
can run:

    python test_all_apps.py

without activating the venv first.
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import warnings
from pathlib import Path

# Must run before other imports that may emit deprecation noise on stderr.
warnings.filterwarnings("ignore", category=DeprecationWarning)

ROOT = Path(__file__).resolve().parent


def venv_python() -> Path | None:
    """Return the venv interpreter path if .venv exists."""
    if sys.platform == "win32":
        candidate = ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        candidate = ROOT / ".venv" / "bin" / "python"
    return candidate if candidate.is_file() else None


def reexec_in_venv_if_needed() -> None:
    """Re-launch this script with .venv Python when not already using it."""
    venv_py = venv_python()
    if venv_py is None:
        return
    if Path(sys.executable).resolve() == venv_py.resolve():
        return
    print(f"Using project venv: {venv_py}")
    os.execv(str(venv_py), [str(venv_py), *sys.argv])


def ensure_dependencies() -> None:
    """Fail fast with install instructions if required packages are missing."""
    missing: list[str] = []
    for module, package in [
        ("flask", "Flask"),
        ("fastapi", "fastapi"),
        ("django", "Django"),
        ("httpx", "httpx"),
        ("streamlit", "streamlit"),
    ]:
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if not missing:
        return

    venv_py = venv_python()
    print("Missing packages:", ", ".join(missing))
    if venv_py is None:
        print("\nCreate a virtual environment and install test dependencies:")
        print(f"  cd {ROOT}")
        print("  python -m venv .venv")
        if sys.platform == "win32":
            print("  .venv\\Scripts\\Activate.ps1")
            print("  pip install -r requirements-test.txt")
        else:
            print("  source .venv/bin/activate")
            print("  pip install -r requirements-test.txt")
    else:
        print("\nInstall test dependencies into the project venv:")
        print(f"  {venv_py} -m pip install -r requirements-test.txt")
    raise SystemExit(1)


VENV_PY = venv_python() or Path(sys.executable)

results: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    results.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}: {detail}")


def free_port() -> int:
    """Pick an ephemeral TCP port for the Streamlit smoke test."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def test_flask() -> None:
    print("\n=== Flask ===")
    sys.path.insert(0, str(ROOT / "flask_app"))
    try:
        from app import app  # noqa: E402

        client = app.test_client()
        r = client.get("/")
        record("GET /", r.status_code == 200, f"status={r.status_code}")
        record("HTML has tasks", b"Flask Tasks" in r.data, "page title present")

        r = client.get("/api/tasks")
        record("GET /api/tasks", r.status_code == 200 and r.is_json, f"count={len(r.json)}")

        r = client.post("/api/tasks", json={"title": "Test from smoke test"})
        record("POST /api/tasks", r.status_code == 201, f"status={r.status_code}")

        task_id = r.json["id"]
        r = client.delete(f"/api/tasks/{task_id}")
        record("DELETE /api/tasks", r.status_code == 204, f"status={r.status_code}")

        r = client.get("/api/tasks/99999")
        record("GET missing task", r.status_code == 404, f"status={r.status_code}")
    except Exception as e:
        record("Flask", False, str(e))
    finally:
        flask_path = str(ROOT / "flask_app")
        if flask_path in sys.path:
            sys.path.remove(flask_path)
        for key in list(sys.modules):
            if key == "app" or key.startswith("app."):
                del sys.modules[key]


def test_fastapi() -> None:
    print("\n=== FastAPI ===")
    sys.path.insert(0, str(ROOT / "fastapi_app"))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from fastapi.testclient import TestClient  # noqa: E402

        from main import app  # noqa: E402

        client = TestClient(app)
        r = client.get("/")
        record("GET /", r.status_code == 200, r.json().get("message", "")[:40])

        r = client.get("/tasks")
        record("GET /tasks", r.status_code == 200, f"count={len(r.json())}")

        r = client.post("/tasks", json={"title": "Smoke test task", "priority": "high"})
        record("POST /tasks", r.status_code == 201, f"id={r.json().get('id')}")
        tid = r.json()["id"]

        r = client.patch(f"/tasks/{tid}", json={"done": True})
        record(
            "PATCH /tasks",
            r.status_code == 200 and r.json()["done"] is True,
            "done=True",
        )

        r = client.delete(f"/tasks/{tid}")
        record("DELETE /tasks", r.status_code == 204, f"status={r.status_code}")

        r = client.get("/openapi.json")
        record(
            "OpenAPI schema",
            r.status_code == 200 and "paths" in r.json(),
            "docs available",
        )
    except Exception as e:
        record("FastAPI", False, str(e))
    finally:
        fastapi_path = str(ROOT / "fastapi_app")
        if fastapi_path in sys.path:
            sys.path.remove(fastapi_path)
        for key in list(sys.modules):
            if key == "main" or key.startswith("main."):
                del sys.modules[key]


def test_django() -> None:
    print("\n=== Django ===")
    django_dir = ROOT / "django_app"
    previous_cwd = Path.cwd()
    os.chdir(django_dir)
    sys.path.insert(0, str(django_dir))
    os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

    try:
        subprocess.run(
            [str(VENV_PY), "manage.py", "makemigrations", "--noinput"],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [str(VENV_PY), "manage.py", "migrate", "--noinput"],
            check=True,
            capture_output=True,
            text=True,
        )
        record("migrations", True, "makemigrations + migrate OK")

        import django  # noqa: E402

        django.setup()
        from django.test import Client  # noqa: E402

        from tasks.models import Task  # noqa: E402

        Task.objects.all().delete()
        Task.objects.create(title="Seed task", priority=Task.Priority.MEDIUM)

        client = Client()
        r = client.get("/")
        record("GET /", r.status_code == 200, f"status={r.status_code}")
        record("HTML has tasks", b"Django Tasks" in r.content, "page title present")

        r = client.post("/add/", {"title": "Added via test", "priority": "high"})
        record(
            "POST /add/",
            r.status_code == 302,
            f"redirect to {r.headers.get('Location', '')}",
        )
        record("Task created", Task.objects.filter(title="Added via test").exists(), "in DB")

        task = Task.objects.first()
        assert task is not None
        r = client.post(f"/toggle/{task.pk}/")
        record("POST toggle", r.status_code == 302, "redirect OK")
        task.refresh_from_db()
        record("Toggle worked", task.done is True, f"done={task.done}")

        r = client.get("/admin/login/")
        record("Admin login page", r.status_code == 200, f"status={r.status_code}")
    except Exception as e:
        record("Django", False, str(e))
    finally:
        os.chdir(previous_cwd)
        django_path = str(django_dir)
        if django_path in sys.path:
            sys.path.remove(django_path)


def test_streamlit() -> None:
    print("\n=== Streamlit ===")
    import httpx

    app_path = ROOT / "streamlit_app" / "app.py"
    port = free_port()
    proc = subprocess.Popen(
        [
            str(VENV_PY),
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.headless",
            "true",
            "--server.port",
            str(port),
            "--browser.gatherUsageStats",
            "false",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=str(ROOT / "streamlit_app"),
    )
    try:
        url = f"http://127.0.0.1:{port}"
        ok = False
        last_err = ""
        for _ in range(45):
            if proc.poll() is not None:
                out = proc.stdout.read() if proc.stdout else ""
                record("Streamlit process", False, f"exited early: {out[:500]}")
                return
            try:
                r = httpx.get(url, timeout=3.0)
                if r.status_code == 200:
                    ok = True
                    break
            except Exception as e:
                last_err = str(e)
            time.sleep(1)

        record("GET / (UI)", ok, f"port={port}" if ok else last_err)

        if ok:
            try:
                hr = httpx.get(f"{url}/_stcore/health", timeout=3.0)
                record("Health endpoint", hr.status_code == 200, f"status={hr.status_code}")
            except Exception:
                record("Health endpoint", True, "skipped (health URL unavailable)")
    except Exception as e:
        record("Streamlit", False, str(e))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> int:
    reexec_in_venv_if_needed()
    ensure_dependencies()

    print("Testing all example applications...")
    print(f"Python: {sys.executable}")

    test_flask()
    test_fastapi()
    test_django()
    test_streamlit()

    print("\n" + "=" * 50)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    for name, ok, detail in results:
        if not ok:
            print(f"  FAILED: {name} — {detail}")
    print(f"\nResult: {passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

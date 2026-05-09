# Backend FastAPI App

This repository contains a FastAPI backend application organized under the `app/` package.

## Run locally

Activate your virtual environment and run:

```bash
uvicorn main:app --reload
```

If you want to run directly from the package, use:

```bash
uvicorn app.main:app --reload
```

## Notes

- The app package is located in `app/`.
- A root-level `main.py` exists to expose the ASGI application for `uvicorn main:app`.
- `.gitignore` already ignores common Python artifacts, virtual environments, logs, and local database files.

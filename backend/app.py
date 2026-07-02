from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "submissions.db"


class AcademyApplication(BaseModel):
    callsign: str = Field(min_length=1, max_length=120)
    age: int = Field(ge=21, le=55)
    experience: int = Field(ge=1, le=50)
    motivation: str = Field(min_length=10, max_length=5000)


class ComplaintSubmission(BaseModel):
    target: str = Field(min_length=1, max_length=120)
    date: str = Field(min_length=4, max_length=32)
    description: str = Field(min_length=10, max_length=8000)
    anonymous: bool = False


app = FastAPI(title="LVPD SWAT API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "https://loorencho.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with db_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS academy_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                callsign TEXT NOT NULL,
                age INTEGER NOT NULL,
                experience INTEGER NOT NULL,
                motivation TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                incident_date TEXT NOT NULL,
                description TEXT NOT NULL,
                anonymous INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            """
        )


@contextmanager
def db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "lvpd-swat-api"}


@app.post("/api/academy")
def submit_academy(payload: AcademyApplication) -> dict[str, Any]:
    created_at = utc_now()
    with db_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO academy_applications (callsign, age, experience, motivation, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload.callsign.strip(),
                payload.age,
                payload.experience,
                payload.motivation.strip(),
                created_at,
            ),
        )
        row_id = cursor.lastrowid

    return {"ok": True, "id": row_id, "message": "Заявка принята SWAT Academy."}


@app.post("/api/complaints")
def submit_complaint(payload: ComplaintSubmission) -> dict[str, Any]:
    created_at = utc_now()
    with db_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO complaints (target, incident_date, description, anonymous, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload.target.strip(),
                payload.date.strip(),
                payload.description.strip(),
                1 if payload.anonymous else 0,
                created_at,
            ),
        )
        row_id = cursor.lastrowid

    return {"ok": True, "id": row_id, "message": "Жалоба зарегистрирована Internal Affairs."}


@app.get("/api/submissions")
def list_submissions(limit: int = 20) -> dict[str, Any]:
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")

    with db_connection() as conn:
        academy = [
            dict(row)
            for row in conn.execute(
                """
                SELECT id, callsign, age, experience, motivation, created_at
                FROM academy_applications
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        ]
        complaints = [
            dict(row)
            for row in conn.execute(
                """
                SELECT id, target, incident_date, description, anonymous, created_at
                FROM complaints
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        ]

    return {"academy": academy, "complaints": complaints}


app.mount("/", StaticFiles(directory=str(ROOT), html=True), name="site")

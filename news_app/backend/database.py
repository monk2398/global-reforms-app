import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "news.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                category TEXT NOT NULL,
                image_url TEXT NOT NULL,
                source TEXT NOT NULL,
                published_at TEXT NOT NULL,
                tags TEXT DEFAULT ''
            )
            """
        )
        conn.commit()


@contextmanager
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_news(payload: dict[str, Any]) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO news (title, summary, category, image_url, source, published_at, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["title"],
                payload["summary"],
                payload["category"],
                payload["image_url"],
                payload["source"],
                payload["published_at"],
                payload.get("tags", ""),
            ),
        )
        return int(cursor.lastrowid)


def list_latest(limit: int = 50) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return list(
            conn.execute(
                "SELECT * FROM news ORDER BY datetime(published_at) DESC LIMIT ?", (limit,)
            )
        )


def list_by_category(category: str, limit: int = 50) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return list(
            conn.execute(
                """
                SELECT * FROM news
                WHERE category = ?
                ORDER BY datetime(published_at) DESC
                LIMIT ?
                """,
                (category, limit),
            )
        )


def get_news_by_id(news_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM news WHERE id = ?", (news_id,)).fetchone()


def update_news(news_id: int, updates: dict[str, Any]) -> bool:
    if not updates:
        return False

    set_clause = ", ".join(f"{key} = ?" for key in updates)
    values = [str(v) if isinstance(v, datetime) else v for v in updates.values()]
    values.append(news_id)

    with get_connection() as conn:
        result = conn.execute(
            f"UPDATE news SET {set_clause} WHERE id = ?",  # nosec B608
            values,
        )
        return result.rowcount > 0


def delete_news(news_id: int) -> bool:
    with get_connection() as conn:
        result = conn.execute("DELETE FROM news WHERE id = ?", (news_id,))
        return result.rowcount > 0


"""Database access for the firmware component inventory.

The database stores component records locally in SQLite.
It contains no API credentials and does not require a database server.
"""

import sqlite3
from pathlib import Path


# Resolve the database location from this file, not the terminal directory.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "data" / "components.db"


def get_connection():
    """Open a SQLite connection and return rows as dictionary-like objects."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the components table if it does not already exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS components (
                component_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                manufacturer TEXT,
                model TEXT,
                quantity INTEGER NOT NULL DEFAULT 0
                    CHECK (quantity >= 0),
                voltage_info TEXT,
                interfaces TEXT,
                notes TEXT
            )
        """)


def list_components() -> dict:
    """Return all inventory records ordered by component name."""
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM components
            ORDER BY name COLLATE NOCASE
        """).fetchall()

    return {
        "count": len(rows),
        "components": [dict(row) for row in rows],
    }


def search_components(keyword: str) -> dict:
    """Search component names, categories, manufacturers, models, and notes."""
    keyword = keyword.strip()

    if not keyword:
        return {
            "count": 0,
            "components": [],
            "message": "Provide a non-empty search keyword.",
        }

    # The query value is parameterized to avoid SQL injection.
    search_pattern = f"%{keyword}%"

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM components
            WHERE name LIKE ?
               OR category LIKE ?
               OR manufacturer LIKE ?
               OR model LIKE ?
               OR interfaces LIKE ?
               OR notes LIKE ?
            ORDER BY name COLLATE NOCASE
        """, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
        )).fetchall()

    return {
        "search_term": keyword,
        "count": len(rows),
        "components": [dict(row) for row in rows],
    }


def get_component_by_id(component_id: int) -> dict:
    """Retrieve one component using its unique database ID."""
    with get_connection() as connection:
        row = connection.execute("""
            SELECT *
            FROM components
            WHERE component_id = ?
        """, (component_id,)).fetchone()

    if row is None:
        return {
            "status": "not_found",
            "message": f"No component found with ID {component_id}.",
        }

    return {
        "status": "success",
        "component": dict(row),
    }
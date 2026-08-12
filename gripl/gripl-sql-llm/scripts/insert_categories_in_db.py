import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "test.db"

categories = [
    "Collection",
    "Storage",
    "Usage",
    "Transferal",
    "Modification",
    "Deletion",
    "Access",
]

connection = sqlite3.connect(DB_PATH)

try:
    cursor = connection.cursor()

    for category in categories:
        cursor.execute(
            """
            INSERT OR IGNORE INTO category (name)
            VALUES (?)
            """,
            (category,)
        )

    connection.commit()

    cursor.execute("SELECT id, name FROM category ORDER BY id")
    rows = cursor.fetchall()

finally:
    connection.close()
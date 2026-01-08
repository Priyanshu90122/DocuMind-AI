import sqlite3
import time

conn = sqlite3.connect("logs.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_type TEXT,
    decision TEXT,
    explanation TEXT,
    processing_time REAL,
    created_at REAL
)
""")
conn.commit()


def save_log(document_type, decision, explanation, processing_time=None):
    cur.execute(
        """
        INSERT INTO logs(
            document_type,
            decision,
            explanation,
            processing_time,
            created_at
        ) VALUES (?,?,?,?,?)
        """,
        (
            document_type,
            decision,
            explanation,
            processing_time,
            time.time()
        )
    )
    conn.commit()

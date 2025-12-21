import sqlite3

conn = sqlite3.connect("logs.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_type TEXT,
    decision TEXT,
    explanation TEXT
)
""")
conn.commit()


def save_log(doc_type, decision, explanation):
    cur.execute(
        "INSERT INTO logs(document_type, decision, explanation) VALUES (?,?,?)",
        (doc_type, decision, explanation)
    )
    conn.commit()

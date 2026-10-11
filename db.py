"""SQLite storage for users and session results."""
import sqlite3
from datetime import datetime

DB_FILE = "app.db"


def _run(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()] if fetch else None
    conn.commit()
    conn.close()
    return rows


def init_db():
    _run("""CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY, salt TEXT, password_hash TEXT)""")
    _run("""CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, created TEXT,
            words INTEGER, wpm REAL, fillers INTEGER,
            pronunciation REAL, grammar_issues INTEGER, transcript TEXT)""")


def get_user(username):
    rows = _run("SELECT * FROM users WHERE username=?", (username,), fetch=True)
    return rows[0] if rows else None


def add_user(username, salt, password_hash):
    _run("INSERT INTO users VALUES (?,?,?)", (username, salt, password_hash))


def save_session(username, r):
    _run("INSERT INTO sessions(username,created,words,wpm,fillers,pronunciation,"
         "grammar_issues,transcript) VALUES (?,?,?,?,?,?,?,?)",
         (username, datetime.now().strftime("%Y-%m-%d %H:%M"), r["word_count"], r["wpm"],
          r["filler_total"], r["pronunciation_score"], len(r["grammar"]), r["transcript"]))


def get_sessions(username):
    return _run("SELECT * FROM sessions WHERE username=? ORDER BY id", (username,), fetch=True)

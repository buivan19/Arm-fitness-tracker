import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('workout_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT,
            reps INTEGER,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_session(exercise_name, reps):
    conn = sqlite3.connect('workout_history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO sessions (exercise_name, reps, timestamp)
        VALUES (?, ?, ?)
    ''', (exercise_name, reps, datetime.now()))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('workout_history.db')
    c = conn.cursor()
    c.execute('SELECT exercise_name, reps, timestamp FROM sessions ORDER BY timestamp DESC')
    data = c.fetchall()
    conn.close()
    return data
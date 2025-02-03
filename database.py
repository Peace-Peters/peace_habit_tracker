import sqlite3

# Create a connection to database
def create_connection():
    return sqlite3.connect("habit_tracker")

def create_tables(cursor):
    # Create the 'habits' table to store user's habits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            habit_period TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            last_completed TEXT,
            streak INTEGER NOT NULL,
            habit_status TEXT NOT NULL
        )
    """)

    # Create the 'tasks' table to store completed habit tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            task_name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            task_log_date TEXT NOT NULL,
            streak INTEGER NOT NULL,
            task_status TEXT NOT NULL
        )
    """)
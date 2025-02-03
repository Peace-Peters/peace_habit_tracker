import pytest
from datetime import datetime
from habit_tracker import MyHabits
from analytics import display_analytics_summary, get_longest_streak_for_habit
from database import create_connection, create_tables


@pytest.fixture(scope='module')
def test_db():
    # Establish Test Database Connection
    dbconnection = create_connection()
    cursor = dbconnection.cursor()

    # Cofigure SQLite for better performance and concurrency
    cursor.execute('PRAGMA journal_mode=WAL;')  
    cursor.execute('PRAGMA synchronous=NORMAL;')  

    # Create tables
    create_tables(cursor)

    # Get current date
    current_date = datetime.now().date().strftime("%Y-%m-%d")

    # Add the starting data
    cursor.execute("""INSERT INTO Habits (habit_name, habit_period, creation_date, last_completed, streak, habit_status) SELECT ?, ?, ?, ?, ?, ? 
    WHERE NOT EXISTS (SELECT 1 FROM Habits WHERE habit_name = ? AND habit_period = ?)""", 
    ("Cycling", "daily", current_date, None, 0, 'active', "Cycling", "daily"))

    cursor.execute("""INSERT INTO Habits (habit_name, habit_period, creation_date, last_completed, streak, habit_status) SELECT ?, ?, ?, ?, ?, ? 
    WHERE NOT EXISTS (SELECT 1 FROM Habits WHERE habit_name = ? AND habit_period = ?)""", 
    ("Hiking", "weekly", current_date, None, 0, 'active', "Hiking", "weekly"))

    dbconnection.commit()
    
    yield dbconnection
    
    dbconnection.close()

@pytest.fixture
def my_habits(test_db):
    return MyHabits(test_db)

def test_add_habit(my_habits, test_db):
    habit_name = "Read Books"
    habit_period = 1

    my_habits.add_habit(habit_name, habit_period)

    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM Habits WHERE habit_name = ?", (habit_name,))
    cursor.fetchone()

def test_deactivate_habit(my_habits, test_db):
    cursor = test_db.cursor()
    cursor.execute("SELECT id FROM Habits WHERE habit_name = ? AND habit_status = 'active'", ("Read Books",))
    habit_id = cursor.fetchone()[0]

    my_habits.deactivate_habit(habit_id)

    cursor.execute("SELECT * FROM Habits WHERE id = ?", (habit_id,))
    cursor.fetchone()

def test_list_all_active_habits(my_habits):
    my_habits.list_all_active_habits()

def test_mark_task_completed(my_habits, test_db):
    cursor = test_db.cursor()

    cursor.execute("SELECT id FROM Habits WHERE habit_name = ?", ("Cycling",))
    cycling_habit_id = cursor.fetchone()[0]
    print(cycling_habit_id)

    my_habits.mark_task_completed(cycling_habit_id)

    cursor.execute("SELECT * FROM Tasks WHERE habit_id = ?", (cycling_habit_id,))
    cursor.fetchone()

    cursor.execute("SELECT id FROM Habits WHERE habit_name = ?", ("Hiking",))
    hiking_habit_id = cursor.fetchone()[0]

    my_habits.mark_task_completed(hiking_habit_id)
    
    cursor.execute("SELECT * FROM Tasks WHERE habit_id = ?", (hiking_habit_id,))
    cursor.fetchone()


def test_get_completed_tasks(my_habits):
    my_habits.get_completed_tasks()

def test_list_all_tasks(my_habits):
    my_habits.list_all_tasks()


def test_display_analytics_summary():
    # Retrieve analytics summary for habits
    display_analytics_summary()

def test_get_longest_streak_for_habit(test_db):
    cursor = test_db.cursor()
    cursor.execute("SELECT id FROM Habits WHERE habit_name = ?", ("Cycling",))
    habit_name = cursor.fetchone()[0]

    get_longest_streak_for_habit(habit_name)


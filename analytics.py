from datetime import datetime, timedelta
from database import create_connection

# Initialize database connection
dbconnection = create_connection()
cursor = dbconnection.cursor()

# Format date
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# Functions for Analyzing Database Data

# Get longest streak
def get_longest_streak():
    result = cursor.execute("SELECT habit_name, MAX(streak) FROM Habits WHERE habit_status = 'active'").fetchone()
    return {"habit_name": result[0], "streak": result[1]} if result else None

# Get all active habits by the periodicity
def get_habits_by_periodicity(periodicity):
    period_map = {1: "daily", 2: "weekly"}
    period = period_map.get(periodicity)
    query = "SELECT habit_name FROM Habits WHERE habit_period = ? AND habit_status = 'active'"
    cursor.execute(query, (period,))
    return [habit[0] for habit in cursor.fetchall()]

# Get Missed Counts for Tasks
def get_missed_counts(habit_name, habit_period, creation_date, interval):
    current_date = datetime.now()
    habit_start_date = max(current_date - timedelta(days=30), datetime.strptime(creation_date, "%Y-%m-%d"))
    
    if habit_period == 'daily':
        tracked_units = (current_date - habit_start_date).days + 1
        query = "SELECT COUNT(DISTINCT task_log_date) FROM Tasks WHERE task_name = ? AND task_log_date BETWEEN ? AND ?"
    elif habit_period == 'weekly':
        start_week = habit_start_date.isocalendar()[1]
        end_week = current_date.isocalendar()[1]
        tracked_units = end_week - start_week + 1

        query = "SELECT COUNT(DISTINCT strftime('%Y-%W', task_log_date)) FROM Tasks WHERE task_name = ? AND task_log_date BETWEEN ? AND ?"
    else:
        raise ValueError("Unsupported habit period")
    
    completed_units = cursor.execute(
        query,
        (habit_name, habit_start_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"))
    ).fetchone()[0]
    
    return tracked_units, completed_units

# Get list of habits user sstruggled with over the last month
def get_struggled_habits():
    struggled_habits = []
    query = "SELECT habit_name, creation_date, habit_period FROM Habits WHERE habit_status = 'active'"
    
    for habit_name, creation_date, habit_period in cursor.execute(query).fetchall():
         # Determine the active duration of the habit
        habit_creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
        days_since_creation = (datetime.now() - habit_creation_date).days

        # Define the interval for tracking missed tasks
        if habit_period == 'daily':
            interval = min(days_since_creation, 30)
        elif habit_period == 'weekly':
            creation_iso_week = habit_creation_date.isocalendar()[1]
            current_iso_week = datetime.now().isocalendar()[1]
            interval = min(current_iso_week - creation_iso_week + 1, 4)
        else:
            raise ValueError("Unsupported habit period")
    
        tracked_units, completed_units = get_missed_counts(habit_name, habit_period, creation_date, interval)

        if completed_units < interval:
            struggled_habits.append(f"The {habit_period} habit {habit_name} has struggled for the past {interval} {'days' if habit_period == 'daily' else 'weeks'} with {tracked_units - completed_units} missed units within this month.")

    return struggled_habits

# Retrieve missed habits from creation date to present
def get_missed_habits():
    missed_habits = []
    query = "SELECT habit_name, creation_date, habit_period FROM Habits WHERE habit_status = 'active'"
    
    for habit_name, creation_date, habit_period in cursor.execute(query).fetchall():
        tracked_units, completed_units = get_missed_counts(habit_name, habit_period, creation_date, interval=None)
        
        if completed_units < tracked_units:
            missed_habits.append(f"The {habit_period} habit {habit_name} was missed {tracked_units - completed_units} times since its creation")
    return missed_habits

# Output data with headers
def display_data(header, data):
    print(header)
    print("        ")
    for item in data:
        print(item)
    print("        ")

# Generate and output the analytics summary to the user
def display_analytics_summary():
    # Longest streak
    longest_streak = get_longest_streak()
    if longest_streak:
        print(f"Longest streak: {longest_streak['streak']} days for habit '{longest_streak['habit_name']}'")
    else:
        print("Longest streak not found.")

    # Active daily habits
    daily_habits = get_habits_by_periodicity(1)
    display_data("Current Daily Habits:", daily_habits)

    # Active weekly habits
    weekly_habits = get_habits_by_periodicity(2)
    display_data("Current Weekly Habits:", weekly_habits)

    # Struggling habits for last month
    struggled_habits = get_struggled_habits()
    display_data("Habits struggled last month:", struggled_habits)

    #Missed habits
    missed_habits = get_missed_habits()
    display_data("Missed Habits:", missed_habits)

# Get longest streak for specific habit
def get_longest_streak_for_habit(habit_name):
    query = "SELECT streak FROM Habits WHERE habit_name = ? AND habit_status = 'active'"
    cursor.execute(query, (habit_name,))
    result = cursor.fetchone()

    if result:
        print("Longest streak for habit", habit_name, "is", result[0])
    else:
        print("No active habit found with the name:", habit_name)
        
    return result[0] if result else 0

# Display active habits
def list_all_active_habits():
    query = "SELECT * FROM Habits WHERE habit_status = 'active'"
    cursor.execute(query)
    return cursor.fetchall()

# Get tasks completed for specific day
def get_completed_tasks_for_date(log_date):
    query = "SELECT * FROM Tasks WHERE task_log_date = ?"
    cursor.execute(query, (log_date,))
    return cursor.fetchall()

# List all tasks completed
def list_all_tasks():
    query = "SELECT * FROM Tasks"
    cursor.execute(query)
    return cursor.fetchall()
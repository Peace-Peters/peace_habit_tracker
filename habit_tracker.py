from datetime import datetime, timedelta
from database import create_connection
from analytics import list_all_active_habits, get_completed_tasks_for_date, list_all_tasks

#Establish Database connection
dbconnection = create_connection()
cursor = dbconnection.cursor()

class Habit:
    def __init__(self, habit_name, habit_period, creation_date=None, habit_status="active"):
        self.id = None 
        self.habit_name = habit_name
        self.habit_period = habit_period
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d")
        self.habit_status = habit_status

    def mark_inactive(self):
        self.habit_status = "inactive"

    def __str__(self):
        return f"Habit(ID: {self.id}, Name: {self.habit_name}, Periodicity: {self.habit_period}, habit_status: {self.habit_status})"


class Task:
    def __init__(self, habit_id, date=None, completed=True):
        self.id = None  
        self.habit_id = habit_id
        self.date = date or datetime.now().date().strftime("%Y-%m-%d")
        self.completed = completed

    def __str__(self):
        return f"Task(ID: {self.id}, Habit ID: {self.habit_id}, Date: {self.date}, Completed: {self.completed})"


class MyHabits:
    def __init__(self, database):
        self.database = database

    def add_habit(self, habit_name, habit_period):
        #Creates and saves a new habit object in the database
         
        if habit_period == 1:
            habit_period = "daily"
        elif habit_period == 2:
            habit_period = "weekly"
        else:
            print("Invalid periodicity. Please input 1 for daily or 2 for weekly.")
            return
        
        new_habit = Habit(habit_name=habit_name, habit_period=habit_period)
        
        query = f"INSERT INTO Habits (habit_name, habit_period, creation_date, last_completed, streak, habit_status) VALUES (?, ?, ?, ?, ?, ?)"
        
        cursor.execute(query, (new_habit.habit_name, new_habit.habit_period, new_habit.creation_date, None, 0, 'active'))
        dbconnection.commit()
        
        new_habit.id = cursor.lastrowid
        print(f"Habit '{new_habit.habit_name}' has been sucessfully added with ID {new_habit.id}.")

    def deactivate_habit(self, habit_id):
        """Finds a habit by ID, marks it inactive, and updates the database."""
        cursor.execute("SELECT * FROM Habits WHERE id = ?", (habit_id,))
        habit_data = cursor.fetchone() 
       
        if habit_data:
            habit_name = habit_data[1]
            query = f"UPDATE Habits SET habit_status = ? WHERE id = ?"
            cursor.execute(query, ('inactive', habit_id))
            dbconnection.commit()
            print(f"Habit '{habit_name}' successfully marked as inactive.")
        else:
            print("Habit not found.")

    def list_all_active_habits(self):
        """Retrieve and list all active habits."""
        habits = list_all_active_habits()
        if habits:
            print("Active Habits:")
            for habit_data in habits:
                print(f"Habit ID: {habit_data[0]}, Habit Name: {habit_data[1]}, Periodicity: {habit_data[2]}, Creation date: {habit_data[3]}, Last Completed: {habit_data[4]}, Streak: {habit_data[5]}, Habit status: {habit_data[6]}")
                print("----------------")
        else:
            print("No active habits found.")

    def list_habits_by_periodicity(self, habit_period):
        """Lists habits by periodicity (daily or weekly) if they are active."""

        period_type = "daily" if habit_period == 1 else "weekly"

        query = "SELECT * FROM Habits WHERE habit_status = ? AND habit_period = ?"
        cursor.execute(query, ("active", period_type))
        filtered_habits = cursor.fetchall()

        if filtered_habits:
            print(f"Active {period_type} Habits:")
            for habit_data in filtered_habits:
                habit_name = habit_data[1] 
                print(f"- {habit_name}")
        else:
            print(f"No active {period_type} habits found.")

    def mark_task_completed(self, habit_id):
        """Creates a Task object for today's date if it's a daily habit or the corresponding date for a weekly habit."""
        cursor.execute("SELECT * FROM Habits WHERE id = ?", (habit_id,))
        habit_data = cursor.fetchone()

        if habit_data:
            today = datetime.now().date().strftime("%Y-%m-%d")
            habit_period = habit_data[2] 
            habit_name = habit_data[1]
            current_streak = habit_data[5]
            habit_status = habit_data[6] 

            # Check if the habit is inactive
            if habit_status != 'active':
                print(f"Habit '{habit_name}' is deactivated and inactive and cannot be marked as completed.")
                return

            if habit_period == 'daily':
                # Check if the task has been completed today
                query = "SELECT * FROM Tasks WHERE habit_id = ? AND periodicity = ? AND task_log_date = ?"
                cursor.execute(query, (habit_id, "daily", today))
                existing_task = cursor.fetchone()

                if existing_task:
                    print(f"Habit '{habit_name}' has already been marked as completed for today.")
                else:
                    new_task = Task(habit_id=habit_id, date=today, completed=True)
                    query = "INSERT INTO Tasks (habit_id, task_name, task_log_date, periodicity, streak, task_status) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(query, (new_task.habit_id, habit_name, new_task.date, "daily", current_streak + 1, "completed"))
                    dbconnection.commit()
                    new_task.id = cursor.lastrowid

                    # Update habit last completed date and streak
                    query_update = "UPDATE Habits SET last_completed = ?, streak = ? WHERE id = ?"
                    cursor.execute(query_update, (today, current_streak + 1, habit_id))
                    dbconnection.commit()

                    print(f"Habit '{habit_name}' marked completed for today. Streak updated to {current_streak + 1}.")

            elif habit_period == 'weekly':
                
                week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).date().strftime("%Y-%m-%d")
                week_end = (datetime.now() + timedelta(days=(6 - datetime.now().weekday()))).date().strftime("%Y-%m-%d")

                # Check if a task for this habit exists within the current week
                query = """
                    SELECT * FROM Tasks
                    WHERE habit_id = ? AND periodicity = ? AND task_log_date BETWEEN ? AND ?
                """
                cursor.execute(query, (habit_id, "weekly", week_start, week_end))
                existing_task = cursor.fetchone()

                if existing_task:
                    print(f"Habit '{habit_name}' has already been marked as completed for this week.")
                else:
                    new_task = Task(habit_id=habit_id, date=today, completed=True)
                    query = "INSERT INTO Tasks (habit_id, task_name, task_log_date, periodicity, streak, task_status) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(query, (new_task.habit_id, habit_name, new_task.date, "weekly", current_streak + 1, "completed"))
                    dbconnection.commit()
                    new_task.id = cursor.lastrowid

                    # Update habit last completed date and streak
                    query_update = "UPDATE Habits SET last_completed = ?, streak = ? WHERE id = ?"
                    cursor.execute(query_update, (today, current_streak + 1, habit_id))
                    dbconnection.commit()

                    print(f"Habit '{habit_name}' marked as completed for the week on {today}. Streak updated to {current_streak + 1}.")

        else:
            print("Habit ID not found.")

    def get_completed_tasks(self, log_date=None):
        """List all tasks completed on a specific date."""
        log_date = log_date or datetime.now().date().strftime("%Y-%m-%d")
        completed_tasks = get_completed_tasks_for_date(log_date)
        
        if completed_tasks:
            print(f"Tasks Completed on {log_date}:")
            for task_data in completed_tasks:
                cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (task_data[1],))
                habit = cursor.fetchone()
                
                if habit:
                    print(f"Task ID: {task_data[0]}, Habit: {habit[0]}, Periodicity: {task_data[3]}, Date: {task_data[4]}, Streak: {task_data[5]}, Task status: {task_data[6]},")
                else:
                    print(f"Habit not found for ID {task_data[1]}")
        else:
            print(f"No tasks completed on {log_date}.")

    def list_all_tasks(self):
        """Retrieve and list all tasks."""
        tasks = list_all_tasks()
        if tasks:
            print("All Tasks:")
            for task_data in tasks:
                cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (task_data[1],))
                habit = cursor.fetchone()
                print(f"Task ID: {task_data[0]}, Habit: {habit[0]}, Periodicity: {task_data[3]}, Date: {task_data[4]}, Streak: {task_data[5]}, Task status: {task_data[6]},")
                print('------------------------------------------------------------------------------')
        else:
            print("No tasks found.")
from habit_tracker import MyHabits
from analytics import display_analytics_summary, get_longest_streak_for_habit
from database import create_connection, create_tables

def main():
    # Initialize database connection
    dbconnection = create_connection()
    cursor = dbconnection.cursor()

    # Create the tables if they do not already exist
    create_tables(cursor)

    my_habits = MyHabits(cursor)

    while True:  
        
        print("\nHabit Tracker CLI:")
        print("Input 1 To Add a New Habit")
        print("Input 2 To Deactivate an Habit")
        print("Input 3 To View all Active Habits")
        print("Input 4 To View Habits by Periodicity")
        print("Input 5 To Mark an Habit Task Completed")
        print("Input 6 To View Tasks Completed for Today")
        print("Input 7 To View all Tasks")
        print("Input 8 To View Habits Analytics")
        print("Input 9 To View the Longest Streak for a Specific Habit")
        print("Input 0 To Exit the Application")

        try:
            menu = int(input("Please input a number between 0 - 9: "))
        except ValueError:
            print("Invalid input! Please input a number between 0 - 9.")
            continue  # Reiterate the loop upon invalid input.

        if menu == 1:
            try:
                habit_name = input("Enter Habit Name: ")
                habit_period = int(input("Periodicity: Enter 1 for Daily; 2 for Weekly: "))
                if habit_period not in [1, 2]:
                    raise ValueError("Invalid periodicity! Please iinput 1 or 2.")
                my_habits.add_habit(habit_name, habit_period)
            except ValueError as e:
                print(e)

        elif menu == 2:
            habit_id = int(input("Enter Habit ID to deactivate: "))
            my_habits.deactivate_habit(habit_id)

        elif menu == 3:
            my_habits.list_all_active_habits()

        elif menu == 4:
            try:
                habit_period = int(input("Periodicity: Enter 1 for Daily; 2 for Weekly: "))
                if habit_period not in [1, 2]:
                    raise ValueError("Invalid periodicity! Please input 1 or 2.")
                my_habits.list_habits_by_periodicity(habit_period)
            except ValueError as e:
                print(e)

        elif menu == 5:
            habit_id = int(input("Enter the ID of the habit: "))
            my_habits.mark_task_completed(habit_id)

        elif menu == 6:
            my_habits.get_completed_tasks()

        elif menu == 7:
            my_habits.list_all_tasks()

        elif menu == 8:
            display_analytics_summary()

        elif menu == 9:
            habit_name = input("Enter the habit name: ")
            get_longest_streak_for_habit(habit_name)

        elif menu == 0:
            print("Application Closed!")
            break  
        else:
            print("Invalid Menu Command!")

    # Disconect database connection
    dbconnection.close()

if __name__ == "__main__":
    main()

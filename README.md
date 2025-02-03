# peace_habit_tracker

# **Habit Tracker CLI Application**

This is a simple command-line interface (CLI) application for creating habits, and tracking them. It is built with Python and SQLite. It helps the user create, manage, and monitor your daily and weekly habits effectively.

## 🚀 **Features**

- Add new habits with custom names and periodicity (daily or weekly)
- Mark habits as completed
- View active habits
- Track streaks for each habit
- Filter habits by periodicity, longest streak, or missed habits
- Deactivate habits without deleting them from the database

## 📦 **Technologies Used**

- **Python**: Core programming language
- **SQLite**: Lightweight database for storing habit data
- **Pytest**: For testing the application

## ⚙️ Installation

1. **Download the project**

- Option 1: Clone the Repository (Recommended)
- Option 2: Download ZIP File from the repository, extract it, and open the folder

2. **Navigate to the Project Folder**

- Open your terminal/command prompt and move to the project directory:

```bash
  cd /path/to/folder
```

3. Run the Application

- Ensure Python 3.7 or higher is installed.
- To start the app run

```bash
python main.py
```

4. Install & Run Tests

- Install pytest (if not already installed) using pip install pytest
- To Run Unit Tests enter

```bash
pytest test.py
```

5. Test Coverage:
   Tests cover functionalities like adding, removing, listing habits, and database operations. Fixtures are used to set up and clean up the testing environment, with assertions to verify correct behavior.

## 📝 **Using the Habit Tracker**

Upon running the app, you’ll see a menu of options. Simply enter the corresponding number and press Enter to perform an action.

Main Menu Options

### **1️⃣ Add a New Habit**

- Purpose: Create a new habit.
- How: Enter the habit’s name and choose its periodicity: 1 for Daily, 2 for Weekly

### **2️⃣ Deactivate an Habit**

- Purpose: Deactivate a habit from your list.
- How: Select the habit by entering its unique ID.

### 3️⃣ View All Active Habits

- Purpose: Display all active habits, including their periodicity and current streaks.

### 4️⃣ Filter Habits by Periodicity

- Purpose: View habits filtered by daily or weekly frequency.
- How: Enter 1 for daily or 2 for weekly habits.

### 5️⃣ Mark Habit Task as Completed

- Purpose: Log a completed habit, automatically updating its streak.
- How: Provide the habit ID to mark it as done.

### 6️⃣ View Today’s Completed Tasks

- Purpose: Check all habits you’ve marked as completed today.

### 7️⃣ View All Logged Tasks

- Purpose: Display a full history of your completed tasks with timestamps.

### 8️⃣ Analyze Habit Data

- Purpose: Get insights into your habit patterns, streaks, and areas for improvement.

### 9️⃣ View Longest Streak for a Habit

- Purpose: See the longest streak achieved for a specific habit.

## 0️⃣ Exit the Application

- Purpose: Close the app safely.

## 🚧 Known Limitations

- Currently supports basic habit tracking for daily and weekly habits only.
- No reminders or notification features (planned for future updates).
- Limited analytics (basic streak and completion tracking).

## 🩺 Troubleshooting

### If App Won’t Start:

- Verify Python 3.7+ is installed with:

```bash
python --version
```

- Try python3 habits.py if python habits.py fails.
- Ensure the main.py file and SQLite database are in the same directory.

### Database Issues:

- Confirm the SQLite database file exists
- Reinitialize the database if corrupted (refer to setup scripts if available).

### Python Not Recognized:

- Add Python to your system’s PATH or reinstall Python with the “Add to PATH” option selected.

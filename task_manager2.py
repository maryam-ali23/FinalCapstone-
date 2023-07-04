import os
import json
from datetime import datetime, date

# Constants
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to read user data from file
def read_users():
    """Read the user data from a file"""
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            data = json.load(file)
            return data
    return {}

# Function to write user data to file
def write_users(data):
    """Write the user data to a file"""
    with open("users.json", "w") as file:
        json.dump(data, file)

# Function to read task data from file
def read_tasks():
    """Read the task data from a file"""
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            data = json.load(file)
            return data
    return []

# Function to write task data to file
def write_tasks(data):
    """Write the task data to a file"""
    with open("tasks.json", "w") as file:
        json.dump(data, file)

# Function to display task details
def display_task(task):
    """Display task details"""
    disp_str = f"Title: {task['title']}\n"
    disp_str += f"Description: {task['description']}\n"
    disp_str += f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Completed: {'Yes' if task['completed'] else 'No'}"
    print(disp_str)

# Function to register a new user
def reg_user():
    """Register a new user"""
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    username_password = read_users()

    if new_password == confirm_password:
        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
        else:
            username_password[new_username] = new_password
            write_users(username_password)
            print("Registration Successful!")
    else:
        print("Passwords do not match.")

# Function to add a new task
def add_task():
    """Add a new task"""
    username = input("Username: ")
    password = input("Password: ")

    username_password = read_users()
    if username in username_password and password == username_password[username]:
        title = input("Task Title: ")
        description = input("Task Description: ")
        due_date_str = input("Due Date (YYYY-MM-DD): ")
        due_date = datetime.strptime(due_date_str, DATETIME_STRING_FORMAT)

        assigned_date = date.today()

        task_list = read_tasks()
        new_task = {
            'username': username,
            'title': title,
            'description': description,
            'due_date': due_date.strftime(DATETIME_STRING_FORMAT),
            'assigned_date': assigned_date.strftime(DATETIME_STRING_FORMAT),
            'completed': False
        }
        task_list.append(new_task)
        write_tasks(task_list)

        print("Task Added Successfully!")
    else:
        print("Invalid username or password.")

# Function to view all tasks
def view_all():
    """View all tasks"""
    task_list = read_tasks()
    if len(task_list) > 0:
        for task in task_list:
            task['due_date'] = datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date()
            task['assigned_date'] = datetime.strptime(task['assigned_date'], DATETIME_STRING_FORMAT).date()
            display_task(task)
            print("--------------------")
    else:
        print("No tasks found.")

# Function to view tasks assigned to the current user
def view_mine():
    """View tasks assigned to the current user"""
    username = input("Username: ")
    password = input("Password: ")

    username_password = read_users()
    if username in username_password and password == username_password[username]:
        user_tasks = [task for task in read_tasks() if task['username'] == username]
        if len(user_tasks) > 0:
            for task in user_tasks:
                task['due_date'] = datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date()
                task['assigned_date'] = datetime.strptime(task['assigned_date'], DATETIME_STRING_FORMAT).date()
                display_task(task)
                print("--------------------")
        else:
            print("No tasks found for the given user.")
    else:
        print("Invalid username or password.")

# Function to generate reports based on tasks and users
def generate_reports():
    """Generate reports based on tasks and users"""
    task_list = read_tasks()
    username_password = read_users()

    if len(task_list) > 0:
        report_str = "Task Reports\n\n"

        for task in task_list:
            task['due_date'] = datetime.strptime(task['due_date'], DATETIME_STRING_FORMAT).date()
            task['assigned_date'] = datetime.strptime(task['assigned_date'], DATETIME_STRING_FORMAT).date()
            report_str += f"Title: {task['title']}\n"
            report_str += f"Assigned to: {task['username']}\n"
            report_str += f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            report_str += f"Completed: {'Yes' if task['completed'] else 'No'}\n"
            report_str += "---------------------\n"

        report_str += "\nUser Reports\n\n"

        for username, _ in username_password.items():
            user_tasks = [task for task in task_list if task['username'] == username]
            report_str += f"Username: {username}\n"
            report_str += f"Number of Tasks: {len(user_tasks)}\n"
            report_str += "---------------------\n"

        with open("reports.txt", "w") as file:
            file.write(report_str)

        print("Reports generated successfully!")
    else:
        print("No tasks found.")

# Function to display statistics from reports.txt file
def display_statistics():
    """Display statistics from reports.txt file"""
    if os.path.exists("reports.txt"):
        with open("reports.txt", "r") as file:
            data = file.read()
            if data:
                print(data)
    else:
        print("Reports file does not exist.")

# Main program loop
def main():
    """Main program loop"""
    while True:
        print("Task Manager\n")
        print("r. Register User")
        print("a. Add Task")
        print("va. View All Tasks")
        print("vm. View My Tasks")
        print("gr. Generate Reports")
        print("ds. Display Statistics")
        print("e. Exit")

        choice = input("Enter your choice: ")

        if choice == "r":
            reg_user()
        elif choice == "a":
            add_task()
        elif choice == "va":
            view_all()
        elif choice == "vm":
            view_mine()
        elif choice == "gr":
            generate_reports()
        elif choice == "ds":
            display_statistics()
        elif choice == "e":
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
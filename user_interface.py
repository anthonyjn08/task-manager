import sys
import datetime
from business_logic import TaskService, UserService
from utilities import date_validation


def login(user_service):
    while True:
        username = input("Username: ")
        password = input("Password: ")
        result = user_service.login(username, password)

        if result == "admin":
            print(f"\n{username} logged in as an admin!\n")
            return "admin"
        elif result == "user":
            print(f"Logged in as {username}.")
            return "user"
        else:
            print("\nIncorrect login. Please try again!\n")

def start_application():
    task_service = TaskService()
    user_service = UserService()

    role, username = login(user_service)

    while True:
        print("Task magaement Application")
        print("Please select one of the following options:")

        print("1. Add task")
        print("2. Get task")
        print("3. View all my tasks")
        print("4. Update task")
        print("5. Mark task complete")

        if role == "admin":
            print("\n***Admin Options***\n")
            print("6. View all tasks")
            print("7. Delete task")
            print("8. View completed tasks")
            print("9. Add user")
            print("10. Update user")
            print("11. Make user an Admin")
            print("12. Delete user")

        print("0. Exit program")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            # Add Task
            print("\nAdd new task\n")
            title = input("Task Title: ")
            description = input("Tasks Description: ")
            assigned_date = datetime.date.today().strftime("%d %b %Y")
            due_date = date_validation("Task due date (e.g., 01 Jan 2000): ")
            user = input("Assigned to: ")
            task_service.add_task(title, description, assigned_date, due_date, user)
        elif choice == 2:
            # Get task
            print("\nGet task\n")
            task_id = int(input("Please enter the task number: "))
            task = task_service.get_task(task_id)
            print(f"Task Number:    {task[0]}   Task Assignee:  {task[5]}")
            print(f"Assigned date:  {task[3]}   Due date:       {task[4]}")
            print(f"Task Title:     {task[1]}")
            print(f"Task Description:")
            print(f"{task[2]}")
        elif choice == 3:
            # View my tasks
            print("\nView my tasks\n")
            tasks = task_service.get_my_tasks(username)
            for task in tasks:
                print("_" * 80)
                print(f"Task Number:    {task[0]}   Task Assignee:  {task[5]}")
                print(f"Assigned date:  {task[3]}   Due date:       {task[4]}")
                print(f"Task Title:     {task[1]}")
                print(f"Task Description:")
                print(f"{task[2]}")
        elif choice == 4:
            # logic
        elif choice == 5:
            # logic
        elif choice == 6:
            # logic
        elif choice == 7:
            # logic
        elif choice == 8:
            # logic
        elif choice == 2:
            # logic
        elif choice == 9:
            # logic
        elif choice == 10:
            # logic
        elif choice == 11:
            # logic
        elif choice == 12:
            # logic
        elif choice == 0:
            sys.exit()
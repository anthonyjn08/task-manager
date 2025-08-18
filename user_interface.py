import sys
import datetime
from business_logic import TaskService, UserService
from utilities import date_validation


# def login(user_service):
#     while True:
#         username = input("Username: ")
#         password = input("Password: ")
#         result = user_service.login(username, password)

#         if result == "admin":
#             print(f"\n{username} logged in as an admin!\n")
#             return "admin"
#         elif result == "user":
#             print(f"Logged in as {username}.")
#             return "user"
#         else:
#             print("\nIncorrect login. Please try again!\n")

def start_application():
    task_service = TaskService()
    user_service = UserService()

    print("Task Management System")
    username = input("Username: ")
    password = input("Password: ")

    user_login = user_service.login(username, password)

    if not user_login:
        print("Invalid login. Please try again.")
        return

    role, username = user_login

    if role == "admin":
        print(f"Welcome {username}. You're logged in as an admin")
    elif role == "user":
        print(f"Welcome {username}")

    while True:
        print("Please select one of the following options:")

        print("1. Add task")
        print("2. Get task")
        print("3. View all my tasks")
        print("4. Update task")
        print("5. Mark task complete")

        if role == "admin":
            print("\n***Admin Options***")
            print("6. View all tasks")
            print("7. Delete task")
            print("8. View completed tasks")
            print("9. Add user")
            print("10. Update user")
            print("11. Make user an Admin")
            print("12. Delete user")
            print("13. Unused")

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
            task_service.add_task(title, description, due_date, assigned_date, user)
        elif choice == 2:
            # Get task
            print("\nGet task\n")
            task_id = int(input("Please enter the task number: "))
            task = task_service.get_task(task_id)
            if task:
                # Print task
                print("Task\n")
                print(f"Task Number: {task["id"]}               Task Assignee: {task["user"]}")
                print(f"Assigned date: {task["assigned_date"]}  Due date: {task["due_date"]}")
                print(f"Task Title: {task["title"]}             Completed: {task["is_complete"]}")
                print(f"Task Description:")
                print(f"{task["description"]}\n")
            else:
                print("Task not found.")
        elif choice == 3:
            # View my tasks
            print("\nView my tasks\n")
            tasks = task_service.get_my_tasks(username)
            if tasks:
                for task in tasks:
                    print("_" * 80)
                    print(f"Task Number: {task[0]}      Task Assignee: {task[6]}")
                    print(f"Assigned date: {task[3]}    Due date: {task[4]}")
                    print(f"Task Title: {task[1]}       Completed: {task[5]}")
                    print(f"Task Description:")
                    print(f"{task[2]}")
        elif choice == 4:
            # Update task
            print("\nUpdate task\n")
            task_id = int(input("Please enter the task number: "))
            task = task_service.get_task(task_id)
            if task:
                # TITLE update
                print(f"Title: {task["title"]}\n")
                while True:
                    update_title = input("Would you like to update the title (y/n): ").lower()
                    if update_title == "y":
                        task["title"] = input("Enter new title: ")
                        break
                    elif update_title == "n":
                        break
                    else:
                        print("Invalid option. Try again")
                
                # DESCRIPTION update
                print(f"Description: {task["description"]}\n")
                while True:
                    update_desc = input("Would you like to update the description (y/n): ").lower()
                    if update_desc == "y":
                        task["description"] = input("Enter new description: ")
                        break
                    elif update_desc == "n":
                        break
                    else:
                        print("Invalid option. Try again")

                # DUE DATE update
                print(f"Due date: {task["due_date"]}\n")
                while True:
                    update_date = input("Would you like to update the due date (y/n): ").lower()
                    if update_date == "y":
                        task["due_date"] = date_validation("Enter new due date: ")
                        break
                    elif update_date == "n":
                        break
                    else:
                        print("Invalid option. Try again")

                # USER update
                print(f"Assigned to: {task["user"]}\n")
                while True:
                    update_user = input("Would you like to update the assigned (y/n): ").lower()
                    if update_user == "y":
                        task["user"] = input("Enter new assignee: ")
                        break
                    elif update_user == "n":
                        break
                    else:
                        print("Invalid option. Try again")
                id = task["id"],
                title = task["title"],
                description = task["description"],
                due_date = task["due_date"],
                user = task["user"]
                task_service.update_task(id, title, description, due_date, user)
            else:
                print("Task not found.")
        elif choice == 5:
            # Mark task complete
            print("\nMark task complete\n")
            task_id = int(input("Please enter the task number: "))
            task = task_service.get_task(task_id)
            if task:
                # Mark Complete
                print(f"Task ID: {task["id"]}       Task Title: {task["title"]}\n")
                while True:
                    complete = input("Mark this task as complete? (y/n): ").lower()
                    if complete == "y":
                        task_service.mark_complete({task_id})
                        break
                    elif complete == "n":
                        break
                    else:
                        print("Invalid option! Try again.")
            else:
                print("Task not found.")
        elif choice == 6:
            # View all tasks
            print("\nView all tasks\n")
            tasks = task_service.view_all_tasks()
            if tasks:
                for task in tasks:
                    print("_" * 80)
                    print(f"Task Number: {task[0]}      Task Assignee: {task[6]}")
                    print(f"Assigned date: {task[3]}    Due date: {task[4]}")
                    print(f"Task Title: {task[1]}       Completed: {task[5]}")
                    print(f"Task Description:")
                    print(f"{task[2]}")
            else:
                print("There are no tasks!")
        elif choice == 7:
            # Delete task
            print("\nDelete Task\n")
            task_id = int(input("Please enter the task number: "))
            task = task_service.get_task(task_id)
            if task:
                # Check if complete or not.
                if task["is_complete"] == 1:
                    status = "Yes"
                else:
                    status = "No"
                # Print task
                print("Task\n")
                print(f"Task Number: {task["id"]}               Task Assignee: {task["user"]}")
                print(f"Assigned date: {task["assigned_date"]}  Due date: {task["due_date"]}")
                print(f"Task Title: {task["title"]}             Completed: {status}")
                print(f"Task Description:")
                print(f"{task["description"]}\n")
            else:
                print("Task not found.")
            print("***WARNING***")
            print("Deleting a task can not be undone!")
            while True:
                confirmation = input(f"Do you want to delete task {task_id}? (y/n): ").lower()
                if confirmation == "y":
                    task_service.delete_task(task_id)
                    print("Task deleted")
                    break
                elif confirmation == "n":
                    break
                else:
                    print("Invalid option! Try again.")
        elif choice == 8:
            # View completed tasks
            print("\nView completed tasks\n")
            tasks = task_service.completed_tasks()
            if tasks:
                for task in tasks:
                    print("_" * 80)
                    print(f"Task Number: {task[0]}      Task Assignee: {task[6]}")
                    print(f"Assigned date: {task[3]}    Due date: {task[4]}")
                    print(f"Task Title: {task[1]}       Completed: {task[5]}")
                    print("Task Description:")
                    print(f"{task[2]}")
            else:
                print("There are no completed tasks!")
        elif choice == 9:
            # Add user
            print("\nAdd user\n")
            username = user_service.validate_user("Enter the username: ")
            password = input("Enter the upassword: ")
            while True:
                email = input("Enter the email address: ")
                if "@" not in email:
                    print("Please enter valid email address.")
                else:
                    break
            user_service.add_user(username, password, email)
        elif choice == 10:
            # Update user
            print("\nUpdate user\n")
            user_id = int(input("Enter user ID: "))
            user = user_service.get_user(user_id)
            if user:
                # USERNAME update
                print(f"Username: {user["username"]}")
                while True:
                    update_username = input("Update username (y/n): ").lower()
                    if update_username == "y":
                        user["username"] = input("Enter new username: ")
                        break
                    elif update_username == "n":
                        break
                    else:
                        print("Invalid option. Try again.")
                # PASSWORD update
                print(f"\nPassword: {user["password"]}")
                while True:
                    update_pwd = input("Update password (y/n): ").lower()
                    if update_pwd == "y":
                        user["password"] = input("Enter new password: ")
                        break
                    elif update_pwd == "n":
                        break
                    else:
                        print("Invalid option. Try again.")

                # EMAIL update
                print(f"Email: {user["email"]}")
                while True:
                    update_email = input("Update email (y/n)").lower()
                    if update_email == "y":
                        user["email"] = input("Enter new email address: ")
                        break
                    elif update_email == "n":
                        break
                    else:
                        print("Invalid option. Try again")
            else:
                print("User not founc.")

            id = user_id
            username = user["username"]
            password = user["password"]
            email = user["email"]
            user_service.update_user(id, username, password, email)
        elif choice == 11:
            # Make user Admin
            print("\nMake user admnin\n")
            user_id = int(input("Enter user ID: "))
            user = user_service.get_user(user_id)
            if user:
                while True:
                    confirm = input(f"Make user {user["username"]} a system"
                                    f" admin? (y/n): ").lower()
                    if confirm == "y":
                        user_service.make_admin(user_id)
                        break
                    elif confirm == "n":
                        break
                    else:
                        print("Invalid Option")
            else:
                print("User not found.")
        elif choice == 12:
            # Delete User
            print("\n Delete user\n")
            user_id = int(input("Enter user ID: "))
            user = user_service.get_user(user_id)
            if user:
                while True:
                    print("WARNING. This can not be undone!")
                    confirm = input(f"Delete user {user["username"]} from"
                                    f" system? (y/n): ").lower()
                    if confirm == "y":
                        user_service.make_admin(user_id)
                        break
                    elif confirm == "n":
                        break
                    else:
                        print("Invalid option. Try again.")
            else:
                print("User not found")
        elif choice == 13:
            # logic
            print("Currently unused.")
        elif choice == 0:
            sys.exit()
        else:
            print("invalid option")
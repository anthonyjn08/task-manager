"""
Provides console based user interface for Task Manager system.

Handles the input/output, menus and interacts with business logic.
"""
import sys
import time
from datetime import datetime, date
from task_manager.business_logic import TaskService, UserService, Task, User
from task_manager.utilities import validate_email, date_validation


def start_application():
    """
    Handles user login, displays user menus based on user role and provides
    interaction between user interface and business logic. Runs in a loop until
    user decides to exit the program."""
    task_service = TaskService()
    user_service = UserService()

    print("Task Management System")
    username = input("Username: ")
    password = input("Password: ")

    user_login = user_service.login(username, password)

    if not user_login:
        print("Invalid login. Please try again.")
        return

    # Get role of user to determine menu displayed
    # Get logged in user to user when updating and viewing tasks
    role, logged_in_user = user_login

    if role == "admin":
        print(f"Welcome {logged_in_user}. You're logged in as an admin")
        time.sleep(1)
    elif role == "user":
        print(f"Welcome {logged_in_user}")
        time.sleep(1)

    while True:
        print("\n*** Main Menu ***")
        print("Please select one of the following options:\n")

        # Standard Menu
        print("0. Exit program")
        print("1. Add task")
        print("2. Get task")
        print("3. View all my tasks")
        print("4. Update task")
        print("5. Mark task complete")

        # Additional admin menu options
        if role == "admin":
            print("\n*** Admin Options ***")
            print("6. View all tasks")
            print("7. Overdue tasks")
            print("8. Completed Tasks")
            print("9. Delete task")
            print("10. Import tasks")
            print("11. Export tasks")
            print("12. View all users")
            print("13. Add user")
            print("14. Update user")
            print("15. Make user an Admin")
            print("16. Delete user")
            print("17. Import users")
            print("18. Export users")

        try:
            choice = int(input("Enter your choice: "))

            # Prevent role "user" accessing admin menu
            if role == "user" and choice > 5:
                print("\nInvalid option, try again.\n")
                continue

            # ********** USER OPTIONS **********
            if choice == 1:
                # Add Task
                print("\nAdd new task\n")
                username = input("Assigned to: ")
                user = user_service.assignee_exists(username)

                # If user doesn' exist, prompted to try again or return
                # to main menu
                while not user:
                    choice = input("\nUser does not exist. Enter a valid "
                                   "username or enter '-1' to return to "
                                   "main menu: ")

                    if choice == "-1":
                        print("Returning to main menu")
                        time.sleep(2)
                        break
                    user = user_service.assignee_exists(choice)

                if not user:
                    continue

                # Task inputs
                title = input("\nTask Title: ")
                description = input("Tasks Description: ")

                # Assigned date auto created using current date
                auto_assigned_date = date.today()

                while True:
                    entered_due_date = input("Task due date "
                                             "(YYYY-MM-DD): ").strip()

                    # Validates that due date is a valid date
                    # Also ensures due date is not before assigned date
                    try:
                        due_date_input = date_validation(entered_due_date)

                        if due_date_input < auto_assigned_date:
                            print("Due date cannot be before assigned date. "
                                  "Please try again.")
                            continue
                        break
                    except ValueError as e:
                        print(f"Invalid date: {e}")

                # Converts data to string format
                assigned_date = auto_assigned_date.strftime("%Y-%m-%d")
                due_date = due_date_input.strftime("%Y-%m-%d")

                new_task = Task(
                    title=title,
                    description=description,
                    assigned_date=assigned_date,
                    due_date=due_date,
                    user=user
                )
                task_id = task_service.add_task(new_task)

                # Confirm task added and provide task number and title
                if task_id:
                    print(f"\nTask {task_id} {title} added to the database.\n")
                else:
                    print("\nFailed to add task! Try again.\n")
                time.sleep(2)

            elif choice == 2:
                # Get task
                print("\nGet task\n")
                while True:
                    try:
                        task_id = int(input("Please enter the task number or "
                                            "-1 for main menu: "))

                        # Return to main menu if user enters -1
                        if task_id == -1:
                            break

                        task = task_service.get_task(task_id)

                        if task:
                            # Print task
                            print("\n" + "-" * 80)
                            print(f"Task Number: {task.task_id}")
                            print(f"Task Assignee: {task.user}")
                            print(f"Assigned date: {task.assigned_date}")
                            print(f"Due date: {task.due_date}")
                            print(f"Task Title: {task.title}")
                            print(f"Completed: {task.is_complete}")
                            print("Task Description:")
                            print(f"{task.description}")
                            print("-" * 80 + "\n")
                            break

                        print("\nThat task doesn't exist.\n")

                    except ValueError:
                        print("\nPlease enter a valid task number!\n")

                time.sleep(2)

            elif choice == 3:
                # View my tasks
                print("\nView my tasks\n")
                tasks = task_service.get_my_tasks(logged_in_user)

                if tasks:
                    for task in tasks:
                        print("-" * 80)
                        print(f"Task Number: {task.task_id}")
                        print(f"Task Assignee: {task.user}")
                        print(f"Assigned date: {task.assigned_date}")
                        print(f"Due date: {task.due_date}")
                        print(f"Task Title: {task.title}")
                        print(f"Completed: {task.is_complete}")
                        print("Task Description:")
                        print(f"{task.description}")
                    print("-" * 80 + "\n")
                else:
                    print("You have no tasks.")

                time.sleep(2)

            elif choice == 4:
                # Update task
                print("\nUpdate task\n")
                while True:
                    try:
                        get_task_id = int(input("Please enter the task number "
                                                "or -1 for main menu: "))

                        # Return to main menu if user enters -1
                        if get_task_id == -1:
                            break

                        task = task_service.get_task(get_task_id)

                        if task:
                            task_id = task.task_id
                            title = task.title
                            description = task.description
                            stored_assigned_date = task.assigned_date
                            due_date = task.due_date
                            is_complete = task.is_complete
                            user = task.user

                            if role == "user":
                                if logged_in_user != user:
                                    print("\nUsers only allowed to edit "
                                          "own tasks!\n")
                                    continue

                            if is_complete == "Yes":
                                print("Completed tasks can not be updated.")
                                continue

                            # TITLE update
                            print(f"\nTitle: {title}")
                            while True:
                                update_title = input("Would you like to update "
                                                     "the title "
                                                     "(y/n): ").lower()

                                if update_title == "y":
                                    title = input("Enter new title: ")
                                    break
                                elif update_title == "n":
                                    break
                                else:
                                    print("Invalid option. Try again")

                            # DESCRIPTION update
                            print(f"\nDescription: {description}")
                            while True:
                                update_desc = input("Would you like to "
                                                    "update the description "
                                                    "(y/n): ").lower()

                                if update_desc == "y":
                                    description = input("Enter new "
                                                        "description: ")
                                    break
                                elif update_desc == "n":
                                    break
                                else:
                                    print("\nInvalid option. Try again\n")

                            # DUE DATE update
                            print(f"\nDue date: {due_date}")
                            while True:
                                update_date = input("Would you like to update "
                                                    "the due date "
                                                    "(y/n): ").lower()

                                if update_date == "y":
                                    while True:
                                        entered_due_date = input("Enter new "
                                                                 "due date: ")

                                        try:
                                            # Date validation and comparison
                                            due_date_input = date_validation(
                                                entered_due_date)
                                            assigned_date = datetime.strptime(
                                                stored_assigned_date, "%Y-%m-%d"
                                                ).date()

                                            if due_date_input < assigned_date:
                                                print("Due date cannot be "
                                                      "before assigned date. "
                                                      "Try again.\n")
                                                continue

                                            due_date = due_date_input.strftime(
                                                "%Y-%m-%d")
                                            assigned_date = (assigned_date
                                                             .strftime(
                                                                 "%Y-%m-%d"))
                                            break

                                        except ValueError as e:
                                            print(f"Invalid date: {e}\n")
                                    break

                                elif update_date == "n":
                                    break
                                else:
                                    print("\nInvalid option. Try again\n")

                            # USER update
                            print(f"\nAssigned to: {user}")
                            while True:
                                update_user = input("Would you like to update "
                                                    "the assigned "
                                                    "(y/n): ").lower()

                                if update_user == "y":
                                    while True:
                                        choice = input("Enter new username: ")
                                        found_user = (
                                            user_service.
                                            assignee_exists(choice))

                                        if found_user:
                                            user = found_user
                                            print(f"Assigned user updated to "
                                                  f"{user}")
                                            break
                                        elif choice == "-1":
                                            print("Keeping existing user!")
                                            break
                                        else:
                                            print("That user does not exist. "
                                                  "Try again or enter '-1' to "
                                                  "keep existing user.")
                                    break

                                elif update_user == "n":
                                    break
                                else:
                                    print("\nInvalid option. Try again\n")

                            updated_task = Task(
                                title=title,
                                description=description,
                                assigned_date=assigned_date,
                                due_date=due_date,
                                user=user,
                                task_id=task_id
                            )

                            if (update_title == "n" and update_desc == "n"
                                    and update_date == "n" and
                                    update_user == "n"):
                                print("Nothing to update. Returning to menu")
                                time.sleep(2)
                                break
                            elif (update_title == "n" and update_desc == "n"
                                    and update_date == "n" and choice == "-1"):
                                print("Nothing to update. Returning to menu")
                                time.sleep(2)
                                break
                            else:
                                update = task_service.update_task(updated_task)

                            if update:
                                print(f"\nTask {task_id}: {title} updated.\n")
                                break
                            else:
                                print(f"\nError! Update failed. Task: "
                                      f"{task_id} not updated.\n")

                        else:
                            print("\nTask doesn't exist.\n")
                            continue

                    except ValueError:
                        print("\nPlease enter a valid task number!\n")

                time.sleep(2)

            elif choice == 5:
                # Mark task complete
                print("\nMark task complete\n")
                while True:
                    try:
                        task_id = int(input("Please enter the task number or "
                                            "-1 for main menu: "))

                        # Return to main menu if user enter -1
                        if task_id == -1:
                            break

                        task = task_service.get_task(task_id)

                        # Exit if task doeesnt exist
                        if not task:
                            print("\nTask does not exist\n")
                            continue

                        if task:
                            # Make sure user it editing their own task
                            if role == "user":
                                if logged_in_user != task.user:
                                    print("\nUsers only allowed to edit "
                                          "own tasks!\n")
                                    continue

                        # If task completed already return to task
                        # number entry
                        if task.is_complete == "Yes":
                            print(f"\nTask {task_id} already completed.\n")
                            continue

                        # Mark Complete
                        print(f"\nTask: {task.task_id} {task.title}\n")
                        while True:
                            complete = input(
                                "Mark this task as complete? "
                                "(y/n): ").lower()

                            if complete == "y":
                                complete = task_service.mark_complete(
                                    task_id)
                                if complete:
                                    print(f"\nTask: {task_id} "
                                          f"{task.title} marked "
                                          f"as complete.\n")
                                    break
                                else:
                                    print(f"\nError! Update failed. Task: "
                                          f"{task_id} not updated.\n")

                            elif complete == "n":
                                break
                            else:
                                print("\nInvalid option! Try again.\n")
                        break
                    except ValueError:
                        print("\nPlease enter a valid task number!\n")

                time.sleep(2)

            # ********** ADMIN OPTIONS **********
            elif choice == 6:
                # ***** View all tasks *****
                print("\nView all tasks\n")
                tasks = task_service.view_all_tasks()
                if tasks:
                    for task in tasks:
                        print("-" * 80)
                        print(f"Task Number: {task.task_id}")
                        print(f"Task Assignee: {task.user}")
                        print(f"Assigned date: {task.assigned_date}")
                        print(f"Due date: {task.due_date}")
                        print(f"Task Title: {task.title}")
                        print(f"Completed: {task.is_complete}")
                        print("Task Description:")
                        print(f"{task.description}\n")
                    print("-" * 80 + "\n")
                else:
                    print("\nThere are no tasks!\n")

                time.sleep(2)

            elif choice == 7:
                # ***** Overdue tasks *****
                print("\nOverdue Tasks\n")
                tasks = task_service.overdue_tasks()

                if tasks is None:
                    print("No overdue tasks.")
                if tasks:
                    for task in tasks:
                        print("-" * 80)
                        print(f"Task Number: {task.task_id}")
                        print(f"Task Assignee: {task.user}")
                        print(f"Assigned date: {task.assigned_date}")
                        print(f"Due date: {task.due_date}")
                        print(f"Task Title: {task.title}")
                        print(f"Completed: {task.is_complete}")
                        print("Task Description:")
                        print(f"{task.description}\n")
                    print("-" * 80 + "\n")
                else:
                    print("\nNo overdue tasks.\n")
                time.sleep(2)

            elif choice == 8:
                # ***** View completed tasks *****
                print("\nView completed tasks\n")
                tasks = task_service.completed_tasks()
                if tasks:
                    for task in tasks:
                        print("-" * 80)
                        print(f"Task Number: {task.task_id}")
                        print(f"Task Assignee: {task.user}")
                        print(f"Assigned date: {task.assigned_date}")
                        print(f"Due date: {task.due_date}")
                        print(f"Task Title: {task.title}")
                        print(f"Completed: {task.is_complete}")
                        print("Task Description:")
                        print(f"{task.description}\n")
                    print("-" * 80 + "\n")
                else:
                    print("There are no completed tasks!")

                time.sleep(2)

            elif choice == 9:
                # ***** Delete task *****
                print("\nDelete Task\n")
                task_id = int(input("Please enter the task number: "))
                task = task_service.get_task(task_id)
                if task:
                    print("-" * 80)
                    print(f"Task Number: {task.task_id}")
                    print(f"Task Assignee: {task.user}")
                    print(f"Assigned date: {task.assigned_date}")
                    print(f"Due date: {task.due_date}")
                    print(f"Task Title: {task.title}")
                    print(f"Completed: {task.is_complete}")
                    print("Task Description:")
                    print(f"{task.description}\n")
                    print("-" * 80 + "\n")
                else:
                    print("\nTask not found. Returning to main menu.\n")
                    time.sleep(2)
                    continue
                print("***WARNING***")
                print("Deleting a task can not be undone!")
                while True:
                    confirmation = input(f"Do you want to delete task "
                                         f"{task_id}: {task.title}? "
                                         f"(y/n): ").lower()

                    if confirmation == "y":
                        deleted = task_service.delete_task(task_id)
                        if deleted:
                            print(f"Task {task_id}: {task.title} "
                                  f"successfully deleted.")
                        else:
                            print(f"Error! Task: {task_id}: {task.title} "
                                  f"not deleted. Try again.")
                        break
                    elif confirmation == "n":
                        break
                    else:
                        print("Invalid option! Try again.")

                time.sleep(2)

            elif choice == 10:
                # ***** Import tasks *****
                print("\nImport Tasks\n")
                print("New tasks will be added to the database.")
                print("Please note, option '4. Update tasks' to update "
                      "existing tasks.\n")
                time.sleep(2)
                task_service.import_tasks()
                print("Tasks Imported.")
                time.sleep(2)

            elif choice == 11:
                # ***** Export tasks *****
                print("\nExport tasks\n")
                task_service.export_tasks()
                time.sleep(2)

            elif choice == 12:
                # ***** View all users *****
                print("\nView all userss\n")
                users = user_service.view_all_users()

                if users:
                    for user in users:
                        print("\n" + "-" * 80)
                        print(f"User ID: {user.user_id}")
                        print(f"Username: {user.username}")
                        print(f"User Email: {user.email}")
                        print(f"Admin User: {user.is_admin}")
                    print("-" * 80 + "\n")

                time.sleep(2)

            elif choice == 13:
                # ***** Add user *****
                print("\nAdd user\n")
                username = user_service.validate_user("Enter the username: ")
                password = input("Enter the upassword: ")
                email = validate_email("Enter the email address: ")

                new_user = User(
                    username=username,
                    password=password,
                    email=email
                )
                user = user_service.add_user(new_user)
                if user:
                    print(f"Print user {user} {username} added.")
                else:
                    print(f"Error occurred, {username} not added. Try again")
                time.sleep(2)

            elif choice == 14:
                # ***** Update user *****
                print("\nUpdate user\n")
                user_id = int(input("Enter user ID: "))
                user = user_service.get_user(user_id)

                if user is None:
                    print("\nUser does not exist.\n")
                    continue

                if user:
                    # USERNAME update
                    print(f"Username: {user.username}")
                    while True:
                        update_username = input(
                            "Update username (y/n): ").lower()
                        if update_username == "y":
                            username = user_service.validate_user(
                                "Enter new username: ")
                            break
                        elif update_username == "n":
                            break
                        else:
                            print("Invalid option. Try again.")

                    # PASSWORD update
                    print(f"\nPassword: {user.password}")
                    while True:
                        update_pwd = input("Update password (y/n): ").lower()
                        if update_pwd == "y":
                            password = input("Enter new password: ")
                            break
                        elif update_pwd == "n":
                            break
                        else:
                            print("Invalid option. Try again.")

                    # EMAIL update
                    print(f"\nEmail: {user.email}")
                    while True:
                        update_email = input("Update email (y/n)").lower()
                        if update_email == "y":
                            email = validate_email(
                                "Enter new email address: ")
                            break
                        elif update_email == "n":
                            break
                        else:
                            print("Invalid option. Try again")
                else:
                    print("User not found.")

                if (update_username == "n" and update_pwd == "n"
                        and update_email == "n"):
                    print("Nothing to update")
                    time.sleep(2)
                    continue

                updated_user = User(
                    username=username,
                    password=password,
                    email=email,
                    user_id=user_id
                )

                update = user_service.update_user(updated_user)
                if update:
                    print(f"User: {user_id} {username} updated.")
                else:
                    print(f"Error occurred, user {user_id} {username} "
                          f"not updated")
                time.sleep(2)

            elif choice == 15:
                # ***** Make user Admin *****
                print("\nMake user admnin\n")
                user_id = int(input("Enter user ID: "))
                user = user_service.get_user(user_id)
                if user:
                    while True:
                        confirm = input(f"Make user {user.username} "
                                        f"a system admin? (y/n): ").lower()
                        if confirm == "y":
                            admin = user_service.make_admin(user_id)
                            if admin:
                                print(f"User: {user_id} {user.username} "
                                      f"made admin.")
                            else:
                                print(f"Error occurred, user {user_id} "
                                      f"{user.username} not updated.")
                            break
                        elif confirm == "n":
                            break
                        else:
                            print("Invalid Option")
                else:
                    print("User not found.")

                time.sleep(2)

            elif choice == 16:
                # ***** Delete User *****
                print("\n Delete user\n")
                try:
                    user_id = int(input("Enter user ID: "))

                    # Ensure admin user can not be deleted
                    if user_id == 1:
                        print("Admin can not be deleted!")
                        time.sleep(2)
                        continue

                    user = user_service.get_user(user_id)
                    if user:
                        while True:
                            print("WARNING. This can not be undone!")
                            confirm = input(f"Delete user {user.username} "
                                            f"from system? (y/n): ").lower()
                            if confirm == "y":
                                delete = user_service.delete_user(user_id)
                                if delete:
                                    print(f"User: {user_id} {user.username} "
                                          f"deleted.")
                                else:
                                    print(f"Error occurred, user {user_id} "
                                          f"{user.username} not deleted.")
                                break
                            elif confirm == "n":
                                break
                            else:
                                print("Invalid option. Try again.")
                    else:
                        print("User not found")
                except ValueError:
                    print("Please enter a valid ID")

                time.sleep(2)

            elif choice == 17:
                # ***** Import users *****
                print("\nImport users\n")
                print("New users will be added to the system.")
                print(
                    "Please note, option '14. Update users' "
                    "to update existing users\n"
                )
                time.sleep(2)
                user_service.import_users()
                time.sleep(2)

            elif choice == 18:
                # ***** Export users *****
                print("\nExport users\n")
                user_service.export_users()
                time.sleep(2)

            elif choice == 0:
                # ***** Exit task manager
                print("Exiting Task Manager")
                time.sleep(1)
                sys.exit()

            else:
                print("Please enter a valid menu option")

        except ValueError:
            print("Please enter a valid menu option")

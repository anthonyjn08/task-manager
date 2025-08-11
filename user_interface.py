from business_logic import TaskService, UserService


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

    role = login(user_service)

    print("Task magaement Application")
    print("Please select one of the following options:")

    print("1. Add task")
    print("2. Get task")
    print("3. View all my tasks")
    print("4. Update task")
    print("5. Mark task complete")

    if role == "admin":
        print("***Admin Options***")
        print("6. View all tasks")
        print("7. Delete task")
        print("8. View completed tasks")
        print("9. Add user")
        print("10. Update user")
        print("11. Make user an Admin")
        print("12. Delete user")

    print("0. Exit program")
        
    

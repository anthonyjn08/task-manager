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

    role = login()

    if login == "admin":
        # admin menu
    elif login == "user":
        # user menu
    elif login == False:
        # try again logic
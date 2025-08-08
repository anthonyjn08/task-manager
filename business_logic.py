from data_access import TaskRepository


class TaskService:
    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.task_repository = TaskRepository()

    def add_task(self, task):
        "Create new task in database"
        self.task_repository.add_task(task)


class Task:
    def __init__(self, title, description, assigned_date, due_date, user):
        """Initialises task object"""
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.user = user


class User:
    def __init__(self, username, password, email, is_admin):
        """Initialises user object"""
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin

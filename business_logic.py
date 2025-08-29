from data_access import TaskRepository, UserRepository


class TaskService:
    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.task_repository = TaskRepository()

    def add_task(self, title, description, due_date, assigned_date,
                 user):
        return self.task_repository.add_task(title, description, assigned_date,
                                      due_date, user)

    def get_task(self, task_id):
        return self.task_repository.get_task(task_id)

    def get_my_tasks(self, user):
        return self.task_repository.get_my_tasks(user)

    def view_all_tasks(self):
        return self.task_repository.view_all_tasks()

    def completed_tasks(self):
        return self.task_repository.completed_tasks()

    def update_task(self, title, description, due_date, user, task_id):
        return self.task_repository.update_task(title, description, due_date,
                                         user, task_id)

    def mark_complete(self, task_id):
        return self.task_repository.mark_complete(task_id)

    def overdue_tasks(self):
        return self.task_repository.overdue_tasks()

    def delete_task(self, id):
        return self.task_repository.delete_task(id)

    def import_tasks(self):
        self.task_repository.import_tasks()

    def export_tasks(self):
        self.task_repository.export_tasks()

class Task:
    def __init__(self, title, description, assigned_date, due_date, user):
        """Initialises task object"""
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.user = user


class UserService:

    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.user_repository = UserRepository()

    def login(self, username, password):
        return self.user_repository.login(username, password)
    
    def view_all_users(self):
        return self.user_repository.view_all_users()

    def add_user(self, username, password, email):
        return self.user_repository.add_user(username, password, email)

    def validate_user(self, prompt):
        return self.user_repository.validate_username(prompt)
    
    def assignee_exists(self, prompt):
        return self.user_repository.assignee_exists(prompt)

    def get_user(self, id):
        return self.user_repository.get_user(id)

    def update_user(self, id, username, password, email):
        return self.user_repository.update_user(id, username, password, email)

    def make_admin(self, id):
        return self.user_repository.make_admin(id)

    def delete_user(self, id):
        return self.user_repository.delete_user(id)

    def import_users(self):
        self.user_repository.import_users()

    def export_users(self):
        self.user_repository.export_users()


class User:
    def __init__(self, username, password, email, is_admin):
        """Initialises user object"""
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin

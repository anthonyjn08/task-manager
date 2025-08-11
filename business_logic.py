from data_access import TaskRepository


class TaskService:
    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.task_repository = TaskRepository()

    def add_task(self, title, description, due_date, assigned_date,
                 user):
        "Add new task in database"
        self.task_repository.add_task(title, description, assigned_date,
                                      due_date, user)

    def get_task(self, task_id):
        return self.task_repository.get_task(task_id)
    
    def get_my_tasks(self, user):
        return self.task_repository.get_my_tasks(user)
    
    def view_all_tasks(self):
        return self.task_repository.view_all_tasks()
    
    def completed_tasks(self):
        return self.task_repository.completed_tasks()
    
    def update_task(self, id, title, description, due_date, user):
        self.task_repository.update_task(id, title, description, due_date,
                                         user)
        
    def mark_complete(self, id):
        self.task_repository.mark_complete(id)

    def delete_task(self, id):
        self.task_repository.delete_task(id)


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

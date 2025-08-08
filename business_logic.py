from data_access import TaskRepository


class TaskService:
    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.task_repository = TaskRepository()

    def add_task(self, task):
        "Create new task in database"
        self.task_repository.add_task(task)

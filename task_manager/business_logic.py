from task_manager.data_access import TaskRepository, UserRepository


class TaskService:
    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.task_repository = TaskRepository()

    def add_task(self, task):
        """
        Adds a new task to the database.
        Calls 'add_task' function from the TaskRepository in data_access.py
        to handle interaction with the database.
        """
        return self.task_repository.add_task(task.title,
                                             task.description,
                                             task.assigned_date,
                                             task.due_date,
                                             task.user
                                             )

    def get_task(self, task_id):
        """
        Retrieves a task in the database using the task_id.
        Calls 'get_task' function from the TaskRepository in data_access.py to
        handle interaction with the database.
        """
        task = self.task_repository.get_task(task_id)
        if not task:
            return None
        
        return Task(
            id=task[0],
            title=task[1],
            description=task[2],
            assigned_date=task[3],
            due_date=task[4],
            is_complete=task[5],
            user=task[6],
        )

    def get_my_tasks(self, user):
        """
        Retrieves all tasks in the database assigned to the logged in user.
        Calls 'get_my_tasks' function from the TaskRepository in data_access.py
        to handle interaction with the database.
        """
        tasks = self.task_repository.get_my_tasks(user)
        if not tasks:
            return []
        
        return [
            Task(
                id=task[0],
                title=task[1],
                description=task[2],
                assigned_date=task[3],
                due_date=task[4],
                is_complete=task[5],
                user=task[6]
            )
            for task in tasks
        ]

    def view_all_tasks(self):
        """
        Allows admins to view all tasks in the database.
        Calls 'view_all' function from the TaskRepository in data_access.py to
        handle interaction with the database.
        """
        tasks = self.task_repository.view_all_tasks()

        if not tasks:
            return []
        
        return [
            Task(
                id=task[0],
                title=task[1],
                description=task[2],
                assigned_date=task[3],
                due_date=task[4],
                is_complete=task[5],
                user=task[6]
            )
            for task in tasks
        ]

    def completed_tasks(self):
        """
        Allows admins to view all completed tasks in the database.
        Calls 'completed_tasks' function from the TaskRepository in
        data_access.py to handle interaction with the database.
        """
        tasks = self.task_repository.completed_tasks()

        if not tasks:
            return []
        
        return [
            Task(
                id=task[0],
                title=task[1],
                description=task[2],
                assigned_date=task[3],
                due_date=task[4],
                is_complete=task[5],
                user=task[6]
            )
            for task in tasks
        ]

    def update_task(self, task):
        """
        Allows users to update the task title, description, due date
        and assignee using the unique task ID. Users can only edit their
        own tasks whilst admins can update all tasks.
        Calls 'update_task' function from the TaskRepository in data_access.py
        to handle interaction with the database.
        """
        return self.task_repository.update_task(task.title,
                                                task.description,
                                                task.due_date,
                                                task.user,
                                                task.id)

    def mark_complete(self, task_id):
        """
        Allows users to mark a task as complete. using the unique task ID.
        Users can only edit their ouw tasks unless they're an admin.
        Calls 'mark_complete' function from the TaskRepository in data_access.py
        to handle interaction with the database.
        """
        return self.task_repository.mark_complete(task_id)

    def overdue_tasks(self):
        """
        Allows admins to view all tasks that are not complete, and the current
        date is after the task due date in the database.
        Calls 'overdue_tasks' function from the TaskRepository in
        data_access.py to handle interaction with the database.
        """
        tasks = self.task_repository.overdue_tasks()

        if not tasks:
            return []

        return [
            Task(
                id=task[0],
                title=task[1],
                description=task[2],
                assigned_date=task[3],
                due_date=task[4],
                is_complete=task[5],
                user=task[6]
            )
            for task in tasks
        ]

    def delete_task(self, id):
        """
        Allows admins to delete a task, if required, using the unique task ID.
        Calls 'delete_task' function from the TaskRepository in
        data_access.py to handle interaction with the database.
        """
        return self.task_repository.delete_task(id)

    def import_tasks(self):
        """
        Allows admins to import task data into the database. New tasks can
        be added, existing tasks are skipped as they're updated using the
        'update_task' function.
        Calls 'import_tasks' function from the TaskRepository in
        data_access.py to handle interaction with the database.
        """
        self.task_repository.import_tasks()

    def export_tasks(self):
        """
        Allows admins to export all task data from the database into a
        text file called 'tasks.txt'.
        Calls 'export_tasks' function from the TaskRepository in
        data_access.py to handle interaction with the database.
        """
        self.task_repository.export_tasks()


class Task:
    def __init__(self, title, description, assigned_date, due_date, user,
                 id=None, is_complete="No"):
        """Initialises task object"""
        self.id = id  # is primary key, only used when reading from DB
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.is_complete = is_complete  # Defaults to 'No' for new tasks.
        self.user = user


class UserService:

    def __init__(self):
        """Initialise the TaskService with a TaskRepository"""
        self.user_repository = UserRepository()

    def login(self, username, password):
        """
        Checks users credentials against to verify login.
        Calls 'login' function from the UserRepository in data_access.py to
        handle interaction with the database.
        """
        return self.user_repository.login(username, password)

    def view_all_users(self):
        """
        Allows admins to view the details of all users in the system.
        Calls 'view_all_users' function from the UserRepository in
        data_access.py to handle interaction with the database.
        """
        users = self.user_repository.view_all_users()

        if not users:
            return []

        return [
            User(
                id=user[0],
                username=user[1],
                password=user[2],
                email=user[3],
                is_admin=user[4],
            )
            for user in users
        ]

    def add_user(self, user):
        """
        Allows admins to add a new user to the system.
        Calls 'add_user' function from the UserRepository in data_access.py to
        handle interaction with the database.
        """
        return self.user_repository.add_user(user.username, user.password,
                                             user.email)

    def validate_user(self, prompt):
        """
        Checks database when adding a new user to ensure the username doesn't
        already exist.
        Calls 'validate_user' function from the UserRepository in
        data_access.py tohandle interaction with the database.
        """
        return self.user_repository.validate_username(prompt)

    def assignee_exists(self, username):
        """
        Checks to make sure that a user exists when they're being assigned
        to a task.
        Calls 'lassignee_exists' function from the UserRepository in
        data_access.py to handle interaction with the database.
        """
        return self.user_repository.assignee_exists(username)

    def get_user(self, id):
        """
        Returns the datails of a user using the unique ID.
        Calls 'get_user' function from the UserRepository in data_access.py to
        handle interaction with the database."""
        user = self.user_repository.get_user(id)

        if not user:
            return None
        
        return User(
            id=user[0],
            username=user[1],
            password=user[2],
            email=user[3],
            is_admin=[4],
        )

    def update_user(self, user):
        """
        Allows admins to update a users details.
        Calls 'update_user' function from the UserRepository in data_access.py
        to handle interaction with the database.
        """
        return self.user_repository.update_user(user.id,
                                                user.username,
                                                user.password,
                                                user.email)

    def make_admin(self, id):
        """
        Allows admins to grant admin privaliges to a user.
        Calls 'make_admin' function from the UserRepository in data_access.py
        to handle interaction with the database.
        """
        return self.user_repository.make_admin(id)

    def delete_user(self, id):
        """
        Allows admins to delete a user from the system.
        Calls 'delete_user' function from the UserRepository in data_access.py
        to handle interaction with the database.
        """
        return self.user_repository.delete_user(id)

    def import_users(self):
        """
        Allows admins to import users from a 'users.txt' file. A new user can
        be added to the system using this.
        Calls 'import_users' function from the UserRepository in data_access.py
        to handle interaction with the database.
        """
        self.user_repository.import_users()

    def export_users(self):
        """
        Allows admins to export all users in the system to a 'users.txt' file.
        Calls 'export_users' function from the UserRepository in data_access.py
        to handle interaction with the database.
        """
        self.user_repository.export_users()


class User:
    def __init__(self, username, password, email,
                 id=None, is_admin="No"):
        """Initialises user object"""
        self.id = id  # Is primary key, only used when reading from DB
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin  # Defaults to 'No' for new users

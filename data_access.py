import sqlite3
from datetime import datetime


class TaskRepository:

    def __init__(self):
        """
        Initialise the Task Repository
        
        Ensures the 'tasks' table exists in the database by calling
        the _create_table() method when a new TaskRepository is created.
        """

        self._create_table()

    def _create_table(self):
        """
        Creates the tasks table, if it does not exist, when called by the __init__
        function"""
        try:
            # Create database called tasks
            db = sqlite3.connect("taskManager.db")

            # Create a cursor object
            cursor = db.cursor()

            # Check for tasks table and create if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS
                tasks(id INTEGER PRIMARY KEY, title TEXT, description TEXT,
                assignedDate TEXT, dueDate TEXT, isComplete TEXt DEFAULT "No",
                user TEXT)
                """
            )

            # Commit the changes
            db.commit()

        # Catch and exceptions
        except sqlite3.Error as e:
            db.rollback()
            print(f"Error creating table: {e}")
            raise
        finally:
            # Close the db connection
            db.close()

    # ********** Task functions **********
    def add_task(self, title, description, assigned_date, due_date, user):
        """
        Function: add_task
        
        This function allows users to create new tasks which are then added to
        the sqlite database.
        
        Input:
        
        - title: (str) Task title.
        - description: (str) Description of the task.
        - assigned_date: (str) Date the task was created. Date is set to task
          creation date automatically.
        - due_date: (str) Date the task needs to be completed by.
        - user: (str) Task assignee.

        Return:

        task_no: (int) Task ID
        """
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                """
                INSERT INTO tasks(title, description, assignedDate, dueDate,
                user)
                VALUES(?, ?, ?, ?, ?)
                """,
                (title, description, assigned_date, due_date, user),
            )
            # Commit the changes
            db.commit()
            task_no = cursor.lastrowid
            return task_no
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            raise
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            raise
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            # Close the db connection
            db.close()

    def get_task(self, task_id):
        """
        Function: get_task

        This function retrieves a task from the sqlite database based on
        its task ID. If the task does not exist, it prints a message
        and returns None.

        Input:

        - task_id: (int) The unique ID of the task to retrieve.

        Return:

        task: If found, returns a dictionary with keys:
            - "id": (int) Task ID
            - "title": (str) Task title
            - "description": (str) Description of the task
            - "assigned_date": (str) Date the task was created
            - "due_date": (str) Date the task is due
            - "is_complete": (str) Completion status ("Yes"/"No")
            - "user": (str) Task assignee

        - None: occurs if the task is not found.
        """

        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        )
        task = cursor.fetchone()
        db.close()

        if task is None:
            print("\nTask not found\n")
            return None

        # Task dictionary
        return {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "assigned_date": task[3],
            "due_date": task[4],
            "is_complete": task[5],
            "user": task[6],
        }

    def get_my_tasks(self, user):
        """
        Function: get_my_tasks

        The functions returns all tasks assigned to the currently logged in user from the
        database.

        Input:

        - user: (str) Username of the logged in user.

        Return:

        - tasks: returns all tasks assigned to user
        - None: occurs if no tasks are found
        """
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE user = ?
            """,
            (user,),
        )
        tasks = cursor.fetchall()
        db.close()

        if tasks is None:
            print("\nYou have no tasks!\n")
            return None

        return tasks

    def view_all_tasks(self):
        """
        Function: view_all_tasks

        Returns all tasks from the database. Available to admins only

        Return:

        - tasks: returns all tasks no matter who they're assigned to
        """
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT *
            FROM tasks
            """
        )
        tasks = cursor.fetchall()
        db.close()

        if tasks is None:
            print("\nThere are currently no tasks!\n")
            return None

        return tasks

    def completed_tasks(self):
        """
        Function: completed_tasks

        Returns all tasks that have been marked as complete. Available to admins only.

        Return:

        - completed_tasks: returns all tasks marked as complete no matter the assignee.
        """
        is_complete = "Yes"
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE isComplete = ?
            """, (is_complete,)
        )
        completed_tasks = cursor.fetchall()
        db.close()

        if completed_tasks is None:
            print("\nThere are currently no completed tasks!\n")

        return completed_tasks

    def update_task(self, title, description, due_date, user, task_id):
        """
        Function: update_task

        Allows users to update an existing task. Title, description, due date, and assignee
        can all be updated. If there are no updates for any of these, the existing data is
        retained. ID/task No. and assigned_date cannot be changed, and is_complete is
        updated in a separate function.

        Input:

        - title: (str) current or new title of the task.
        - description: (str) current or new description of the task.
        - due_date: (str) current or updated due date in "%d/%m/%Y" format.
        - user: (str) current or updated task assignee.
        - task_id: (int) ID of the task to update.

        Return:

        task_id: (int) the ID of the updated task.
        """
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE tasks
                SET title = ?, description = ?, dueDate = ?, user = ?
                WHERE id = ?''',
                (title, description, due_date, user, task_id)
            )
            db.commit()
            return task_id
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            raise
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            raise
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            db.close()

    def mark_complete(self, task_id):
        """
        Function: mark_complete

        Marks selected task as complete.

        Input:

        - task_id: (int) ID of the task to mark as complete.
        """       
        try:
            is_complete = "Yes"
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE tasks
                SET isComplete = ?
                WHERE id = ?
                ''',
                (is_complete, task_id)
            )
            db.commit()
            print(f"Task {task_id} marked as complete.")
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            raise
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            raise
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            db.close()

    def overdue_tasks(self):
        """
        Function: overdue_tasks

        Returns all tasks that are incomplete and the due date has passed. Available to
        admins only.

        Return:

        - overdue_tasks: returns all overdue tasks.
        - None: occurs when there are no overdue tasks
        """    
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE dueDate < DATE("now") AND isComplete = "No"
            """
        )
        overdue_tasks = cursor.fetchall()
        db.close()

        if overdue_tasks is None:
            print("No overdue tasks.")
            return None

        return overdue_tasks
    
    def delete_task(self, id):
        """
        Function: delete_task

        Deletes selected task from the database. Available to admins only.

        Input:

        - id: (int) ID of the task to delete.
        """
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                DELETE FROM tasks
                WHERE ID = ?
                ''', (id,)
            )
            # Commit the changes
            db.commit()
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            raise
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            raise
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            db.close()
            print(f"Task {id} deleted")

    def import_tasks(self):
        """
        Function: import_tasks

        Imports tasks from a 'tasks.txt' file into the database. Tasks with invalid
        dates or where user doesn't exist are skipped. Updates to existing tasks are
        also skipped and users are warned of this. Available to admins only.
        """
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()

        with open("tasks.txt", "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                try:
                    task = line.strip().split(",")
                    
                    if len(task) != 7:
                        print(f"{line.strip()} skipped due to incorrect format.")
                        continue

                    id = int(task[0].strip())
                    title = task[1].strip()
                    description = task[2].strip()
                    assigned_date = task[3].strip()
                    due_date = task[4].strip()
                    is_complete = task[5].strip()
                    user = task[6].strip()

                    try:
                        assigned_date = datetime.strptime(assigned_date.strip(), "%d/%m/%Y").strftime("%d/%m/%Y")
                        due_date = datetime.strptime(due_date.strip(), "%d/%m/%Y").strftime("%d/%m/%Y")
                    except ValueError:
                        print(f"Task {id} skipped: Incorrect date format")
                        continue

                    cursor.execute(
                        '''
                        SELECT id FROM user
                        WHERE username = ?
                        ''', (user.strip(), )
                    )

                    user_exist = cursor.fetchone()

                    if not user_exist:
                        print(f"Task {id} skipped: {user} does not exist.")
                        continue

                    try:
                        cursor.execute(
                            '''
                            INSERT INTO tasks(id, title, description, assignedDate, dueDate, isComplete,
                            user)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(id) DO NOTHING
                            ''', (id, title, description, assigned_date, due_date, is_complete, user)
                        )
                    except sqlite3.IntegrityError as e:
                        db.rollback()
                        print(f"Integrity error: {e}")
                        raise
                    except sqlite3.OperationalError as e:
                        db.rollback()
                        print(f"Operational error: {e}")
                        raise
                    except sqlite3.DatabaseError as e:
                        db.rollback()
                        print(f"Database error: {e}")
                        raise
                
                except ValueError:
                    print(f"{line.strip()} skipped due to incorrect format.")
                    continue

        db.commit()
        db.close()
        print("\nTasks imported.\n")

    def export_tasks(self):
        """
        Function: export_tasks

        Exports all tasks from the database to a 'tasks.txt' file. Available to
        admin users only.
        """
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            '''
            SELECT * FROM tasks
            '''
        )
        tasks = cursor.fetchall()

        with open("tasks.txt", "w", encoding="utf-8") as file:
            for task in tasks:
                id, title, description, assigned_date, due_date, is_complete, user = task

                line = (f"{id},{title},{description},{assigned_date},{due_date},"
                        f"{is_complete},{user}")

                file.write(line+"\n")

        db.close()

        print(f"All tasks exported successfully. Total: {len(tasks)} tasks.")


class UserRepository:

    def __init__(self):
        self._create_table()

    def _create_table(self):
        try:
            # Create database called tasks
            db = sqlite3.connect("taskManager.db")

            # Create a cursor object
            cursor = db.cursor()

            # Check for table called users and create if it does not exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS
                user(id INTEGER PRIMARY KEY, username TEXT UNIQUE,
                password TEXT,
                email TEXT, isAdmin TEXT DEFAULT "No")
                """
            )

            # Check count of users and if 0 add admin user
            cursor.execute(
                '''
                SELECT COUNT(*)
                FROM user
                '''
            )
            user_count = cursor.fetchone()

            if user_count[0] == 0:

                # Admin variables
                username = "admin"
                password = "admin"
                email = "test@test.com"
                is_admin = "Yes"

                cursor.execute(
                    '''
                    INSERT INTO user(username, password, email, isAdmin)
                    VALUES(?, ?, ?, ?)
                    ''', (username, password, email, is_admin)
                )

                # Commit the changes
                db.commit()

        # Catch and exceptions
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    # User functions

    def login(self, username, password):
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM user
            WHERE username = ?
            ''', (username,)
        )

        user = cursor.fetchone()
        db.close()

        if user is None:
            return None

        is_admin = user[4]
        stored_password = user[2]
        if stored_password == password and is_admin == "Yes":
            role = "admin"
            return role, password
        elif stored_password == password:
            role = "user"
            return role, password
        else:
            print("Incorrect password.")

    def view_all_users(self):
        
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM user
            '''
        )
        users = cursor.fetchall()
        db.close()

        return users

    def add_user(self, username, password, email):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                INSERT INTO user(username, password, email)
                VALUES(?, ?, ?)
                ''', (username, password, email)
            )
            # Commit the changes
            db.commit()
            user_id = cursor.lastrowid
            print(f"\nUser {user_id}: {username} successfully added.\n")
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def validate_username(self, prompt):
        while True:
            username = input(prompt)
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                SELECT *
                FROM user
                WHERE username = ?
                ''', (username,)
            )
            user = cursor.fetchone()
            db.close()
            if user:
                print("Username already exists. Please choose again")
                continue
            return username

    def assignee_exists(self, prompt):
        # while True:
        username = input(prompt)
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM user
            WHERE username = ?
            ''', (username,)
        )
        user = cursor.fetchone()
        db.close()
        if not user:
            print("Assignee does not exist. Please create the assignee then"
                  " try again.")
            return None
        return username

    def get_user(self, id):
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM user
            WHERE id = ?
            ''', (id,)
        )
        user = cursor.fetchone()
        db.close()

        if user is None:
            return None
        else:
            return {
                "id": user[0],
                "username": user[1],
                "password": user[2],
                "email": user[3],
                "admin": user[4]
            }

    def update_user(self, id, username, password, email):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE user
                SET username = ?, password = ?, email = ?
                WHERE id = ?
                ''', (username, password, email, id)
            )
            # Commit the changes
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def make_admin(self, id):
        try:
            is_admin = "Yes"
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE user
                SET isAdmin = ?
                WHERE id = ?
                ''', (is_admin, id)
            )
            # Commit the changes
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def delete_user(self, id):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                DELETE FROM user
                WHERE id = ?
                ''', (id,)
            )
            # Commit the changes
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

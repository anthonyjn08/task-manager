import sqlite3
import re
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
        Creates the tasks table, if it does not exist, when called by
        the __init__ function.
        """
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

        Output:
        - cursor.lastrowid: returns the id of new task if added
        - None: occurs if a sqlite3 error happens
        """
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                """
                INSERT INTO tasks(title, description, assignedDate, dueDate,
                user)
                VALUES(?, ?, ?, ?, ?)
                """, (title, description, assigned_date, due_date, user)
            )
            # Commit the changes
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
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

        Output:
        - task: If found, returns a dictionary with keys:
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

        The functions returns all tasks assigned to the currently logged in
        user from the database.

        Input:
        - user: (str) Username of the logged in user.

        Output:
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
            return None

        return tasks

    def view_all_tasks(self):
        """
        Function: view_all_tasks

        Returns all tasks from the database.
        Available to admins only

        Output:
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
            return None

        return tasks

    def completed_tasks(self):
        """
        Function: completed_tasks

        Returns all tasks that have been marked as complete.
        Available to admins only.

        Output:
        - completed_tasks: returns all tasks marked as complete no matter
          the assignee.
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
            return None

        return completed_tasks

    def update_task(self, title, description, due_date, user, task_id):
        """
        Function: update_task

        Allows users to update an existing task. Title, description, due date
        and assignee can all be updated. If there are no updates for any of
        these, the existing data is retained. ID/task No. and assigned_date
        cannot be changed, and is_complete is updated in a separate function.

        Input:
        - title: (str) current or new title of the task.
        - description: (str) current or new description of the task.
        - due_date: (str) current or updated due date in "%d/%m/%Y" format.
        - user: (str) current or updated task assignee.
        - task_id: (int) ID of the task to update.

        Output:
        - cursor.rowcount: if more than 0 the update was completed
          else it failed
        - None: occurs if there is a sqlite3 error or update failed
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
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def mark_complete(self, task_id):
        """
        Function: mark_complete

        Marks selected task as complete.

        Input:
        - task_id: ID of task to be marked as complete

        Output:
        - cursor.rowcount: if more than 0 the update was completed,
          else it failed
        - None: occurs if there is a sqlite3 error
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
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def overdue_tasks(self):
        """
        Function: overdue_tasks

        Returns all tasks that are incomplete and the due date has passed.
        Available to admins only.

        Output:
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
            return None

        return overdue_tasks

    def delete_task(self, id):
        """
        Function: delete_task

        Deletes selected task from the database. Available to admins only.

        Input:
        - id: (int) ID of the task to delete.
        - None: occurs if there is a sqlite3 error

        Output:
        - cursor.rowcount: if more than 0 the deletion was completed,
          else it failed
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
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def import_tasks(self):
        """
        Function: import_tasks

        Imports tasks from a 'tasks.txt' file into the database. Existing
        tasks are skipped, as they're updated using'update_task'. New tasks
        can be added if they meet validation rules. Tasks with invalid dates
        or where user doesn't exist are skipped, with a message printed to
        the console for each task that is skipped. Available to admins only.

        Output:
        - None: occurs if there is a sqlite3 error
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
                        print(f"{line.strip()} skipped due to incorrect"
                              f" format.")
                        continue

                    id = int(task[0].strip())
                    title = task[1].strip()
                    description = task[2].strip()
                    assigned_date = task[3].strip()
                    due_date = task[4].strip()
                    is_complete = task[5].strip().capitalize()
                    user = task[6].strip()

                    try:
                        assigned_date = datetime.strptime(
                            assigned_date.strip(), "%d/%m/%Y").strftime(
                                "%d/%m/%Y")
                        due_date = datetime.strptime(
                            due_date.strip(), "%d/%m/%Y").strftime(
                                "%d/%m/%Y")
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
                            INSERT INTO tasks(id, title, description,
                            assignedDate, dueDate, isComplete, user)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(id) DO NOTHING
                            ''', (id, title, description, assigned_date,
                                  due_date, is_complete, user)
                        )
                    except sqlite3.IntegrityError as e:
                        db.rollback()
                        print(f"Integrity error: {e}")
                        return None
                    except sqlite3.OperationalError as e:
                        db.rollback()
                        print(f"Operational error: {e}")
                        return None
                    except sqlite3.DatabaseError as e:
                        db.rollback()
                        print(f"Database error: {e}")
                        return None

                except ValueError:
                    print(f"{line.strip()} skipped due to incorrect format.")
                    continue

        db.commit()
        db.close()

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
                (id, title, description, assigned_date, due_date,
                 is_complete, user) = task

                line = (f"{id},{title},{description},{assigned_date},"
                        f"{due_date}, {is_complete},{user}")

                file.write(line+"\n")
        db.close()
        print(f"All tasks exported successfully. Total: {len(tasks)} tasks.")


class UserRepository:

    def __init__(self):
        """
        Initialise the User Repository

        Ensures the 'user' table exists in the database by calling
        the _create_table() method when a new UserRepository is created.
        """
        self._create_table()

    def _create_table(self):
        """
        Creates the user table, if it does not exist, when called by
        the __init__ function. It then adds 'admin' user to the database so the
        system can be accessed.
        """
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

                try:
                    cursor.execute(
                        '''
                        INSERT INTO user(username, password, email, isAdmin)
                        VALUES(?, ?, ?, ?)
                        ''', (username, password, email, is_admin)
                    )

                except sqlite3.IntegrityError as e:
                    db.rollback()
                    print(f"Integrity error: {e}")
                except sqlite3.OperationalError as e:
                    db.rollback()
                    print(f"Operational error: {e}")
                except sqlite3.DatabaseError as e:
                    db.rollback()
                    print(f"Database error: {e}")

                # Commit the changes
                db.commit()

        # Catch and exceptions
        except sqlite3.Error as e:
            db.rollback()
            print(f"Error creating table: {e}")
        finally:
            # Close the db connection
            db.close()

    # User functions

    def login(self, username, password):
        """
        Function: login

        This function checks a user’s details in the database to allow login.
        Upon login the users role is determined between 'user' and 'admin' who
        have more persmissions than standard users.

        Input:
        - username: (str) The username of the user attempting to log in.
        - password: (str) The password associated with the user account.

        Output:
        - role: (str) Returns the users role on successful login,
          which determines menu options.
        """
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
        """
        Function: view_all_users

        This function queries the database and returns all current users.
        Available to admins only.

        Output:
        - users: returns all active users.
        """
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
        """
        Function: add_user

        This function adds a new user to the database.
        Available to admins only.

        Input:
        - username: (str) The username of the new user.
        - password: (str) The password for the new user.
        - email: (str) The email address of the new user.

        Output:
        - cursor.lastrowid: returns the ID (primary key) of last entry into
          user table.
        """
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                INSERT INTO user(username, password, email)
                VALUES(?, ?, ?)
                ''', (username, password, email)
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def validate_username(self, prompt):
        """
        Function: validate_username

        This function prompts for and validates a new username against existing
        entries in the database. if user already exists, user is told to enter
        a unique username.

        Input:
        - prompt: (str) A message shown to the user when asking for input.

        Output:
        - username: (str) If username is unique, this is returned.
        """
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

    def assignee_exists(self, username):
        """
        Function: assignee_exists

        This function checks if the provided username for either
        a new or updated task already exists in the database. If not,
        users are prompted to add a valid assignee.

        Input:
        - prompt: (str) A message shown to the user when asking for input.

        Output:
        - username: (str) The existing username if found.
        - None: If the username does not exist.
        """
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
            return None

        return user[1]

    def get_user(self, id):
        """
        Function: get_user

        This function returns the details of user with entered ID.

        Input:
        - id: (int) The user ID.

        Output:
        - user: (dict) A dictionary containing user details if found.
            -   "id": (int) users unique ID
            -   "username": (str) users username, must be unique
            -   "password": (str) users password
            -   "email": (str) users email address
            -   "admin": (str) Yes or No depeing on if user is an admin or not
        - None: If no user is found with the entered ID.
        """
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
        """
        Function: update_user

        This function updates the details of an existing user in the database.
        Users can choose what they need to update. If a field  doesn't need
        updating the existing data is retained.
        Available to admins only.

        Input:
        - id: (int) The ID of the user to update.
        - username: (str) The updated/existing username.
        - password: (str) The updated/existing password.
        - email: (str) The updated/existing email address.

        Output:
        - cursor.rowcount: If > 0 update was completed else it failed.
        """
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
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def make_admin(self, id):
        """
        Function: make_admin

        This function updates selected user to gain admin privileges.
        Available to admins only.

        Input:
        - id: (int) ID of the user to promote.

        Output:
        - cursor.rowcount: If > 0 update was completed else it failed.
        """
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
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def delete_user(self, id):
        """
        Function: delete_user

        This function deletes a user from the database by their ID.
        Available to admins only.

        Input:
        - id: (int) The ID of the user to delete.

        Output:
        - cursor.rowcount: If rowcount > 0 user was deleted else
          the deletion failed.
        """
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                DELETE FROM user
                WHERE id = ?
                ''', (id,)
            )
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            db.rollback()
            print(f"Integrity error: {e}")
            return None
        except sqlite3.OperationalError as e:
            db.rollback()
            print(f"Operational error: {e}")
            return None
        except sqlite3.DatabaseError as e:
            db.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            db.close()

    def import_users(self):
        """
        Function: import_users

        This function imports user records from a 'users.txt' file into the
        database.
        It checks IDs, usernames, and email to ensure they valid before
        insertion.
        Any updates are skipped as well as updates handled in separate
        function.
        Available to admins only.
        """
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()

        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                try:
                    user = line.strip().split(",")

                    if len(user) != 5:
                        print(f"{line.strip()} skipped due to"
                              f" incorrect format.")
                        continue

                    id = int(user[0].strip())
                    username = user[1].strip()
                    password = user[2].strip()
                    email = user[3].strip()
                    is_admin = user[4].strip().capitalize()

                    # Validate email address, skip line where not valid
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        print(f"User: {id} {username} skipped. "
                              f"Incorrect email format")
                        continue

                    # Check for iD and username already existing,
                    # Skip where ID or user name conflict happen
                    cursor.execute(
                        """
                        SELECT id, username
                        FROM user
                        WHERE id = ? OR username = ?
                        """, (id, username)
                    )

                    users_check = cursor.fetchall()

                    conflict = False
                    for user in users_check:
                        exist_id, exist_username = user
                        if exist_id == id and exist_username != username:
                            print(f"User: {id} {username} skipped. "
                                  f"ID in use by {exist_id} {exist_username}")
                            conflict = True
                        elif exist_username == username and exist_id != id:
                            print(f"User: {id} {username} skipped. "
                                  f"Username used by user ID "
                                  f"{exist_id} {exist_username}")
                            conflict = True

                    if conflict:
                        continue

                    try:
                        cursor.execute(
                            """
                            INSERT INTO user(id, username, password, email,
                            isAdmin)
                            VALUES (?, ?, ?, ?, ?)
                            ON CONFLICT(id) DO NOTHING
                            """, (id, username, password, email, is_admin)
                        )
                    except sqlite3.IntegrityError as e:
                        db.rollback()
                        print(f"Integrity error: {e}")
                        return None
                    except sqlite3.OperationalError as e:
                        db.rollback()
                        print(f"Operational error: {e}")
                        return None
                    except sqlite3.DatabaseError as e:
                        db.rollback()
                        print(f"Database error: {e}")
                        return None

                except ValueError:
                    print(f"{line.strip()} skipped. Invalid ID format")
                    continue

        db.commit()
        db.close()

    def export_users(self):
        """
        Function: export_users

        This function exports all user records from the database into a
        'users.txt' file.
        Available to admins only.
        """
        db = sqlite3.connect("taskManager.db")
        cursor = db.cursor()
        cursor.execute(
            '''
            SELECT * FROM user
            '''
        )
        users = cursor.fetchall()

        with open("users.txt", "w", encoding="utf-8") as file:
            for user in users:
                id, username, password, email, is_admin = user

                line = (f"{id},{username},{password},{email},{is_admin}")

                file.write(line+"\n")

        db.close()

        print(f"All users exported successfully. Total: {len(users)} users.")

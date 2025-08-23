import sqlite3
from datetime import datetime


class TaskRepository:

    def __init__(self):
        self._create_table()

    def _create_table(self):
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
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    # Task functions

    def add_task(self, title, description, assigned_date, due_date, user):
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
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def get_task(self, task_id):
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

        return tasks

    def view_all_tasks(self):
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

        return tasks

    def completed_tasks(self):
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
            # Commit the changes
            db.commit()
            return task_id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def mark_complete(self, task_id):
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
            # Commit the changes
            db.commit()
            print(f"Task {task_id} marked as complete.")
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def overdue_tasks(self):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                """
                SELECT *
                FROM tasks
                WHERE dueDate < DATE("now") AND isComplete = "No"
                """
            )
            tasks = cursor.fetchall()
            db.close()

            if tasks is None:
                print("No overdue tasks.")
                return None

            return tasks
        except Exception as e:
            raise e

    def delete_task(self, id):
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
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()


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
            print("User successfully added.")
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

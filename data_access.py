import sqlite3


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
                assignedDate TEXT, dueDate TEXT, isComplete BOOLEAN DEFAULT 0,
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
        all_tasks = cursor.fetchall()

        if all_tasks is None:
            print("\nThere are currently no tasks!\n")

        return all_tasks
    
    def completed_tasks(self):
        is_complete = True
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

        if completed_tasks is None:
            print("\nThere are currently no completed tasks!\n")

        return completed_tasks

    def update_task(self, task_id, title, description, due_date, user):
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
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def mark_complete(self, id):
        try:
            is_complete = 1
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE tasks
                SET isComplete = ?
                WHERE id = ?
                ''',
                (is_complete, id)
            )
            # Commit the changes
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

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
                user(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT,
                email TEXT, isAdmin TEXT)
                """
            )

            # Check count of users and if 0 add admin user
            cursor.execute(
                '''
                SELECT COUNT(*)
                FROM users
                '''
            )
            user_count = cursor.fetchone()
            
            if user_count[0] == 0:

                # Admin variables
                username = "admin"
                password = "admin"
                email = "test@test.com"
                isAdmin = 1

                cursor.executemany(
                    '''
                    INSERT INTO users(username, password, email, isAdmin)
                    VALUES(?, ?, ?, ?)
                    ''', (username, password, email, isAdmin)
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
            FROM users
            WHERE username = ?
            ''', (username,)
        )

        user = cursor.fetchone()

        if user is None:
            return False

        if user[2] == password and user[4] == 1:
            return "admin"
        elif user[2] == password:
            return "user"

    def add_user(self, username, password, email):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                INSERT INTO users(username, password, email)
                VAULEs(?, ?, ?)
                ''', (username, password, email)
            )
            # Commit the changes
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()

    def update_user(self, id, username, password, email):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE users
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
            is_admin = 1
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE users
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
                DELETE FROM users
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

import sqlite3


class TaskRepository:

    try:
        # Create database called tasks
        db = sqlite3.connect("taskManager.db")

        # Create a cursor object
        cursor = db.cursor()

        # Check for table called task and create if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            user(id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT,
            isAdmin TEXT)
            """
        )

        # Check for tasks table and create if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            tasks(id INTEGER PRIMARY KEY, title TEXT, description TEXT, assignedDate TEXT,
            dueDate TEXT, isComplete BOOLEAN DEFAULT 0, user TEXT)
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

        if task is None:
            print("\nTask not found\n")

        return task

    def update_task(self, id, title, description, due_date, user):
        try:
            db = sqlite3.connect("taskManager.db")
            cursor = db.cursor()
            cursor.execute(
                '''
                UPDATE tasks
                SET title = ?, description = ?, dueDate = ?, user = ?
                WHERE id = ?''',
                (title, description, due_date, user, id)
            )
        except Exception as e:
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()
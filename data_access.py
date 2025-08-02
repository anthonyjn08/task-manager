import sqlite3


class TaskRepository:

    try:
        # Create database called tasks
        db = sqlite3.connect("tasks.db")

        # Create a cursor object
        cursor = db.cursor()

        # Check for table called task and create if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            user(id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT,
            isAdmin INTEGER)
            """
        )

        # Check for tasks table and create if it does not exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            tasks(id INTEGER PRIMARY KEY, title TEXT, description TEXT,assignedDate TEXT,
            dueDate TEXT, status TEXT, isComplete TEXT, user TEXT)
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

"""
Unit tests for the TaskService class in the task_manager project.

Enter "python -m unittest tests.test" into console to run tests.
"""
import unittest
from task_manager.business_logic import TaskService, UserService, Task, User

# Creating the task and user services
task_service = TaskService()
user_service = UserService()


class TestTaskService(unittest.TestCase):
    """
    Unit testing of the TaskService class.
    Tests will validate that core features of the task management system
    work.
    Methods tested are add_task and update_tasks.
    """
    def test_add_task(self):
        """Test the add_task method of TaskService"""
        # Arrange
        # Get initial task count
        initial_task_count = len(task_service.view_all_tasks())

        new_task = Task(
            title="unit tests",
            description="unit testing",
            assigned_date="2025-09-03",
            due_date="2025-09-03",
            user="admin"
        )

        # Act
        task_service.add_task(new_task)

        # Assert
        # Get updated task count
        updated_task_count = len(task_service.view_all_tasks())

        # Check if task count increased by 1
        self.assertEqual(
            updated_task_count, initial_task_count + 1
        )

        # Check new task is in the list of tasks using title
        all_tasks = task_service.view_all_tasks()

        titles = [task.title for task in all_tasks]
        self.assertIn(new_task.title, titles)

    def test_update_task(self):
        """Test the update_task method of TaskService"""
        # Arrange
        # Get task id
        all_tasks = task_service.view_all_tasks()

        for task in all_tasks:
            if task.title == "unit tests":
                updated_task = task
                break

        updated_task = Task(
            title="updated unit tests",
            description="updated unit testing",
            assigned_date=updated_task.assigned_date,
            due_date=updated_task.due_date,
            user=updated_task.user,
            task_id=updated_task.task_id
        )

        # Act
        task_service.update_task(updated_task)

        # Assert
        # Check if task was updated with title check
        all_tasks = task_service.view_all_tasks()

        for task in all_tasks:
            if task.task_id == updated_task.task_id:
                updated_title = task.title
                break

        self.assertEqual(updated_task.title, updated_title)


class TestUserService(unittest.TestCase):
    """
    Unit testing of the UserService class.
    Tests will validate that core features of the task management system
    work.
    Methods tested are add_user and delete_user.
    """
    def test_add_user(self):
        """Test the add_user method of UserService"""
        # Arrange
        # Get initial user count
        initial_user_count = len(user_service.view_all_users())

        new_user = User(
            username="unittester",
            password="tester",
            email="unittester@test.com",
            is_admin="No"
        )

        # Act
        user_service.add_user(new_user)

        # Assert
        # Get updated user count
        updated_user_count = len(user_service.view_all_users())

        # Check original user count increased by 1
        self.assertEqual(
            updated_user_count, initial_user_count + 1
        )

        # Check new user was added using username
        all_users = user_service.view_all_users()

        usernames = [user.username for user in all_users]
        self.assertIn(new_user.username, usernames)

    def test_delete_user(self):
        """Test the delete_user method in UserService"""
        # Arrange
        # Get initial user count
        initial_user_count = len(user_service.view_all_users())

        # Get user ID
        all_users = user_service.view_all_users()

        for user in all_users:
            if user.username == "unittester":
                user_id = user.user_id
                break

        # Act
        user_service.delete_user(user_id)

        # Assert
        # Get updated user count
        updated_user_count = len(user_service.view_all_users())

        # Check if user count decreased by 1
        self.assertEqual(
            updated_user_count, initial_user_count - 1
        )

        # Check user is no longer in user list
        updated_all_users = user_service.view_all_users()

        user_ids = [user.user_id for user in updated_all_users]
        self.assertNotIn(user_id, user_ids)


if __name__ == "__main__":
    unittest.main()

import unittest
from task_manager.business_logic import TaskService, UserService


class TestTaskService(unittest.TestCase):
    def test_add_task(self):
        task_service = TaskService()
        initial_task_count = len(task_service.view_all_tasks())

        title = "unittesting"
        description = "Unittesting"
        assigned_date = "02/09/2025"
        due_date = "03/09/2025"
        user = "admin"

        new_task = task_service.add_task(title, description, assigned_date,
                                         due_date, user)

        updated_task_count = len(task_service.view_all_tasks())

        self.assertEqual(
            updated_task_count, initial_task_count + 1
        )

        self.assertIn(
            (13, 'unittesting', 'Unittesting', '02/09/2025', '03/09/2025', 'No', 'admin'), task_service.view_all_tasks()
        )


# class TestUserService(unittest.TestCase):
#     def test_add_user(self):
#         user_service = UserService()
#         initial_user_count = len(user_service.view_all_users())

#         username = "tester"
#         password = "home"
#         email = "mo@arsenal.com"

#         new_user = user_service.add_user(username, password, email)

#         updated_user_count = len(user_service.view_all_users())

#         self.assertEqual(
#             updated_user_count, initial_user_count + 1
#         )

#         self.assertIn(
#             (7, 'test', 'home', 'mo@arsenal.com', 'No'), user_service.view_all_users()
#         )


if __name__ == "__main__":
    unittest.main()

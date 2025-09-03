from task_manager.user_interface import start_application


if __package__ is None or __package__ == "":
    # Running main.py directly (F5 / python main.py)
    from user_interface import start_application
else:
    # Running as a package (python -m task_manager.main)
    from task_manager.user_interface import start_application

if __name__ == "__main__":
    start_application()

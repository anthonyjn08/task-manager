import re
from datetime import datetime


def validate_email(prompt):
    while True:
        email = input(prompt)

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format. Try again")
            continue

        return email


def date_validation(prompt):
    '''
    Function: date_validation
    This function converts the string date when adding tasks into an
     acutal date format that can be used when checking if a task
     is overdue.

    Input:
    prompt: (str) asks users to input a date.

    Output:
    date_obj: (date) returns the user string in date format
    '''
    while True:
        date_input = input(prompt)

        try:
            date_obj = datetime.strptime(date_input.strip(), "%d/%m/%Y")
            return date_obj

        except ValueError:
            print("\nPlease enter a date in following format: 'DD/MM/YYYY'.\n")
import re
from datetime import datetime


def validate_email(prompt):
    """
    Function: validate_email

    This function ensures that there is text before and after the '@' symbol
    for email adresses.

    Input:
    - prompt: user is given a prompt to enter the email address

    Output:
    - email: valid email address is returned. Invalid emails triggers message
      to enter email addtress again
    """
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

    This function converts the string date when adding tasks into an acutal
    date format that can be used when adding or updating tasks.

    Input:
    - prompt: (str) asks users to input a date.

    Output:
    - date_obj: (date) returns the user string in date format
    '''
    while True:
        date_input = input(prompt)

        try:
            date_obj = datetime.strptime(date_input.strip(), "%d/%m/%Y")
            return date_obj

        except ValueError:
            print("\nPlease enter a date in following format: 'DD/MM/YYYY'.\n")

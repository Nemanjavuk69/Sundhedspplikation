import re  # Importing the re module for regular expression operations


# Defining the function to check if a password is valid
def is_valid_password(password):
    """
    Check if the password is between 8 and 16 characters long.

    Parameters:
    password (str): The password to validate.

    Returns:
    bool: True if the password is valid, False otherwise.
    """
    return bool(re.fullmatch(r'.{8,16}', password))  # Using regular expression to check the password length


# Defining the function to check if a password is strong
def is_strong_password(password):
    """
    Check if the password meets the following criteria:
    - Contains at least one special character from [!, ", #, %, &, /, (, ), =, ?, *]
    - Does not contain three consecutive digits in strictly increasing or decreasing order
    - Contains at least one uppercase letter
    """
    if not re.search(r'[!"#%&/()=?*]', password):  # Checking if the password contains at least one special character
        return False  # Returning False if no special character is found
    # Checking if the password contains sequential digits
    if check_sequential_digits(password) == False:
        return False  # Returning False if sequential digits are found
    # Checking if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False  # Returning False if no uppercase letter is found
    return True  # Returning True if all criteria are met


# Defining the function to check for sequential digits in the password
def check_sequential_digits(password):
    for i in range(len(password) - 2):  # Iterating through the password
        # Checking if the current substring of 3 characters are digits
        if password[i:i+3].isdigit():
            # Finding all characters in the substring
            digits = re.findall(r'.', password[i:i+3])
            # Checking for strictly increasing order
            if int(digits[1]) == int(digits[0])+1 and int(digits[2]) == int(digits[0])+2:
                return False  # Returning False if strictly increasing order is found
            # Checking for strictly decreasing order
            elif int(digits[1]) == int(digits[0])-1 and int(digits[2]) == int(digits[0])-2:
                return False  # Returning False if strictly decreasing order is found
    return True  # Returning True if no sequential digits are found


def is_valid_email(email):  # Defining the function to check if an email is valid
    """
    Validates the email to ensure it follows specific rules:
    - Starts with a string, contains '@', followed by a string,
    - Ends with .dk, .com, .org, or .aau

    Parameters:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(dk|com|org|aau)$'  # Defining the regular expression pattern for email validation
    # Using regular expression to validate the email
    return bool(re.match(pattern, email))


# Printing the result of is_valid_password function for testing
print(is_valid_password("Hejsa6969!"))

import secrets  # Importing the secrets module for generating secure tokens
import smtplib  # Importing the smtplib module for sending emails
# Importing MIMEText for email text content
from email.mime.text import MIMEText
# Importing MIMEMultipart for multipart email messages
from email.mime.multipart import MIMEMultipart
# Optionally, import os if you're using environment variables
# import os


def generate_secure_code():  # Defining the function to generate a secure code
    code = secrets.token_hex(3)  # Generates a 6-character hexadecimal string
    return code  # Returning the generated code


# Defining the function to send a code via email
def send_code_via_email(receiver_email, code):

    # Setting the sender's email address
    sender_email = "Nemanjavuksanovic69@gmail.com"
    # Consider using environment variables or a secrets manager
    sender_password = r"dnqv eqkw wjod zvnc"  # Setting the sender's email password

    # Creating a multipart email message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Login Code"  # Setting the email subject
    # Setting the sender's email address in the message
    message["From"] = sender_email
    # Setting the receiver's email address in the message
    message["To"] = receiver_email

    text = f"""\
    Hi,
    Your login code is {code}. This code expires in 10 minutes.
    """  # Creating the email text content
    part = MIMEText(
        text, "plain")  # Creating a MIMEText object for plain text content
    message.attach(part)  # Attaching the text part to the message

    # Replace 'smtp.example.com' with your actual email provider's SMTP server
    # Example for Gmail  # Creating an SMTP SSL connection
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # Logging into the email server
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email,
                    message.as_string())  # Sending the email
    server.quit()  # Closing the connection to the server


def verify_code(input_code, correct_code):  # Defining the function to verify the code
    # Returning True if the input code matches the correct code, otherwise False
    return input_code == correct_code


# Example Usage
if __name__ == "__main__":  # Checking if the script is run directly
    # Prompting the user to enter their email
    receiver_email = input("Enter your email: ")
    generated_code = generate_secure_code()  # Generating a secure code
    # Sending the generated code via email
    send_code_via_email(receiver_email, generated_code)
    # Informing the user that the code has been sent
    print("A verification code has been sent to your email. Please check your inbox.")

    for _ in range(3):  # Allow up to 3 attempts
        # Prompting the user to enter the verification code
        user_code = input("Please enter the verification code: ")
        # Checking if the entered code is correct
        if verify_code(user_code, generated_code):
            # Informing the user of successful verification
            print("Verification successful!")
            break  # Exiting the loop
        else:
            # Informing the user of incorrect code
            print("Incorrect code, please try again.")
    else:
        # Informing the user that verification failed after 3 attempts
        print("Verification failed after 3 attempts.")

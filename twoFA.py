import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Optionally, import os if you're using environment variables
# import os


def generate_secure_code():
    code = secrets.token_hex(3)  # Generates a 6-character hexadecimal string
    return code


def send_code_via_email(receiver_email, code):

    sender_email = "Nemanjavuksanovic69@gmail.com"
    # Consider using environment variables or a secrets manager
    sender_password = r"dnqv eqkw wjod zvnc"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Login Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Hi,
    Your login code is {code}. This code expires in 10 minutes.
    """
    part = MIMEText(text, "plain")
    message.attach(part)

    # Replace 'smtp.example.com' with your actual email provider's SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Example for Gmail
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


def verify_code(input_code, correct_code):
    return input_code == correct_code


# Example Usage
if __name__ == "__main__":
    receiver_email = input("Enter your email: ")
    generated_code = generate_secure_code()
    send_code_via_email(receiver_email, generated_code)
    print("A verification code has been sent to your email. Please check your inbox.")

    for _ in range(3):  # Allow up to 3 attempts
        user_code = input("Please enter the verification code: ")
        if verify_code(user_code, generated_code):
            print("Verification successful!")
            break
        else:
            print("Incorrect code, please try again.")
    else:
        print("Verification failed after 3 attempts.")

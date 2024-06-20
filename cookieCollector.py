from flask import Flask, session  # Importing Flask and session from Flask
# Importing SecureCookieSessionInterface for session handling
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)  # Creating an instance of the Flask class
# Replace with your actual Flask secret key
app.secret_key = '123456'  # Setting the secret key for the Flask app


# Defining a function to decode a Flask session cookie
def decode_flask_cookie(cookie):
    """Decode a Flask session cookie"""
    cookie = '.eJxNjLsKwkAQRX9lnDoEsUylCFaWYiMhLJtZM2azK_sISMi_O5EErGbuvZwzYWOsih1FrB4TQpKD7IzHAq_-yQ5i1ppiNNmWcO5I9_DxOQANii0YHyB1BIfLCbRvqcR6LjbNSoppme8U2LBWif2_dCdEXeBPhxU6edxLjbk_Wh6p1H4QPkcKDbey77cUvCXJb_GRS2vr1LCUN4oJ5y-TH0nB.ZiwfIQ.-IIbr5kjDYbs_L6FJZpsL5t5TBg'  # Example session cookie
    try:
        # Use Flask's session cookie decoder
        # Creating an instance of SecureCookieSessionInterface
        session_cookie = SecureCookieSessionInterface()
        # Getting the signing serializer from the session cookie interface
        serializer = session_cookie.get_signing_serializer(app)
        # Decoding the cookie using the serializer
        return serializer.loads(cookie)
    except Exception as e:  # Handling exceptions during decoding
        # Returning an error message if decoding fails
        return f"Failed to decode cookie: {e}"


# Example cookie string
cookie_str = '.eJxNjLsKwkAQRX9lnDoEsUylCFaWYiMhLJtZM2azK_sISMi_O5EErGbuvZwzYWOsih1FrB4TQpKD7IzHAq_-yQ5i1ppiNNmWcO5I9_DxOQANii0YHyB1BIfLCbRvqcR6LjbNSoppme8U2LBWif2_dCdEXeBPhxU6edxLjbk_Wh6p1H4QPkcKDbey77cUvCXJb_GRS2vr1LCUN4oJ5y-TH0nB.ZiwfIQ.-IIbr5kjDYbs_L6FJZpsL5t5TBg'  # Setting an example cookie string
# Decoding the example cookie string
decoded_cookie = decode_flask_cookie(cookie_str)
print(decoded_cookie)  # Printing the decoded cookie

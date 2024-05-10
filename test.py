from flask import Flask, session
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
# Replace with your actual Flask secret key
app.secret_key = '123456'


def decode_flask_cookie(cookie):
    """Decode a Flask session cookie"""
    cookie = '.eJxNjLsKwkAQRX9lnDoEsUylCFaWYiMhLJtZM2azK_sISMi_O5EErGbuvZwzYWOsih1FrB4TQpKD7IzHAq_-yQ5i1ppiNNmWcO5I9_DxOQANii0YHyB1BIfLCbRvqcR6LjbNSoppme8U2LBWif2_dCdEXeBPhxU6edxLjbk_Wh6p1H4QPkcKDbey77cUvCXJb_GRS2vr1LCUN4oJ5y-TH0nB.ZiwfIQ.-IIbr5kjDYbs_L6FJZpsL5t5TBg'
    try:
        # Use Flask's session cookie decoder
        session_cookie = SecureCookieSessionInterface()
        serializer = session_cookie.get_signing_serializer(app)
        return serializer.loads(cookie)
    except Exception as e:
        return f"Failed to decode cookie: {e}"


# Example cookie string
cookie_str = '.eJxNjLsKwkAQRX9lnDoEsUylCFaWYiMhLJtZM2azK_sISMi_O5EErGbuvZwzYWOsih1FrB4TQpKD7IzHAq_-yQ5i1ppiNNmWcO5I9_DxOQANii0YHyB1BIfLCbRvqcR6LjbNSoppme8U2LBWif2_dCdEXeBPhxU6edxLjbk_Wh6p1H4QPkcKDbey77cUvCXJb_GRS2vr1LCUN4oJ5y-TH0nB.ZiwfIQ.-IIbr5kjDYbs_L6FJZpsL5t5TBg'
decoded_cookie = decode_flask_cookie(cookie_str)
print(decoded_cookie)

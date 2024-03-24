from flask import Blueprint, request, flash, redirect, url_for, session, render_template
import csv
from twoFA import generate_secure_code, send_code_via_email
from hashing import hash_string
from salting import salt

login_blueprint = Blueprint('login_blueprint', __name__)


def verify_user_credentials(username, hashed_password):
    with open('users.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Username'] == username and row['Password'] == hashed_password:
                return True, row['Email']
    return False, None


@login_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_string(password + salt())
    user_verified, user_email = verify_user_credentials(
        username, hashed_password)

    if user_verified:
        code = generate_secure_code()
        send_code_via_email(user_email, code)
        session['2fa_code'] = code
        flash('Login successful. Check your email for the 2FA code.', 'info')
        return redirect(url_for('login_blueprint.login_control'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login_blueprint.login'))


@login_blueprint.route('/loginControl', methods=['GET', 'POST'])
def login_control():
    # Initialize tries in session if not set
    if 'tries' not in session:
        session['tries'] = 3

    if request.method == 'POST':
        input_code = request.form['code']
        correct_code = session.get('2fa_code', '')

        if input_code == correct_code:
            # Clear the 2FA code and tries from the session after successful verification
            session.pop('2fa_code', None)
            session.pop('tries', None)
            flash('2FA Verification successful!', 'success')
            return redirect(url_for('yay'))
        else:
            session['tries'] -= 1
            flash('Invalid 2FA code. Please try again.', 'error')

            if session['tries'] <= 0:
                # Clear tries to reset for the next login attempt
                session.pop('tries', None)
                # Optionally clear 2FA code if you don't want it to linger
                session.pop('2fa_code', None)
                flash('You have exceeded the number of attempts.', 'error')
                return redirect(url_for('sad'))

    return render_template('loginControl.html')

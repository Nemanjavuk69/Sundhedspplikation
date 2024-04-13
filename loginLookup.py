from flask import Blueprint, request, flash, redirect, url_for, session, render_template
import csv
from twoFA import generate_secure_code, send_code_via_email
from hashing import hash_string
from salting import salt
from healthJournal import get_health_journal  # Make sure to import this here
from flask import jsonify  # Add this import if it's not already there

login_blueprint = Blueprint('login_blueprint', __name__)


def verify_user_credentials(username, hashed_password):
    with open('users.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Username'] == username and row['Password'] == hashed_password:
                print(row['ID'])
                return True, row['Email'], row['ID']
    return False, None


@login_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_string(password + salt())
    user_verified, user_email, user_id = verify_user_credentials(
        username, hashed_password)

    if user_verified:
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = user_email
        code = generate_secure_code()
        send_code_via_email(user_email, code)
        session['2fa_code'] = code
        session['tries'] = 3  # Initialize the number of tries for 2FA
        flash('Login successful. Check your email for the 2FA code.', 'info')
        return redirect(url_for('login_blueprint.login_control'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('sad'))


@login_blueprint.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login_blueprint.login'))

    journal_entries = get_health_journal(user_id)
    return render_template('dashboard.html', entries=journal_entries)


@login_blueprint.route('/loginControl', methods=['GET', 'POST'])
def login_control():
    if request.method == 'POST':
        input_code = request.form['code']
        correct_code = session.get('2fa_code', '')

        if input_code == correct_code:
            # Clear the 2FA code and tries from the session after successful verification
            session.pop('2fa_code', None)
            session.pop('tries', None)
            flash('2FA Verification successful!', 'success')
            # Updated this line
            return redirect(url_for('login_blueprint.dashboard'))
        else:
            session['tries'] -= 1
            if session['tries'] > 0:
                flash(f'Invalid 2FA code. {
                      session["tries"]} attempts left.', 'error')
            else:
                session.pop('tries', None)
                session.pop('2fa_code', None)
                flash('You have exceeded the number of attempts.', 'error')
                # Use the correct blueprint namespace
                return redirect(url_for('login_blueprint.sad'))

    return render_template('loginControl.html')


@login_blueprint.route('/get-journal-entries')
def get_journal_entries():
    user_id = session.get('user_id')
    if not user_id:
        # Return empty and unauthorized if no user ID is found
        return jsonify([]), 401

    entries = get_health_journal(user_id)
    return jsonify(entries)


@login_blueprint.route('/send-message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'success': False}), 403  # Not authorized or no session

    data = request.get_json()
    message = data['message']
    username = session['username']
    user_id = session['user_id']
    email = session['email']

    # Save to CSV, assuming you have added error handling and CSV headers previously
    with open('inquiry.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, user_id, email, message])

    return jsonify({'success': True})

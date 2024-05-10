from flask import Blueprint, request, flash, redirect, url_for, session, render_template
import csv
from twoFA import generate_secure_code, send_code_via_email
from hashing import hash_string
from salting import salt
from healthJournal import get_health_journal  # Make sure to import this here
from flask import jsonify  # Add this import if it's not already there

login_blueprint = Blueprint('login_blueprint', __name__)


def verify_user_credentials(username, hashed_password, user_type='patient'):
    csv_file = 'doctors.csv' if user_type == 'doctor' else 'users.csv'
    with open(csv_file, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Username'] == username and row['Password'] == hashed_password:
                return True, row['Email'], row['ID']
    return False, None, None


@login_blueprint.route('/login/patient', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_string(password + salt())
        user_verified, user_email, user_id = verify_user_credentials(
            username, hashed_password, user_type='patient')

        if user_verified:
            session.clear()  # Clear previous session before setting new values
            session['user_id'] = user_id
            session['username'] = username
            session['email'] = user_email
            session['user_role'] = 'patient'  # Explicitly set the user role
            code = generate_secure_code()
            send_code_via_email(user_email, code)
            session['2fa_code'] = code
            session['tries'] = 3  # Initialize the number of tries for 2FA
            flash('Login successful. Check your email for the 2FA code.', 'info')
            # Redirect to 2FA verification page
            return redirect(url_for('login_blueprint.login_control'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('patientLogin.html')
    else:
        return render_template('patientLogin.html')


@login_blueprint.route('/login/doctor', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_string(password + salt())
        user_verified, user_email, user_id = verify_user_credentials(
            username, hashed_password, user_type='doctor')

        if user_verified:
            session.clear()  # Clear previous session before setting new values
            session['user_id'] = user_id
            session['username'] = username
            session['email'] = user_email
            session['user_role'] = 'doctor'  # Identify the user as a doctor
            code = generate_secure_code()
            send_code_via_email(user_email, code)
            session['2fa_code'] = code
            session['tries'] = 3
            flash('Login successful. Check your email for the 2FA code.', 'info')
            return redirect(url_for('login_blueprint.login_control_doctor'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('doctorLogin.html')
    else:
        return render_template('doctorLogin.html')


@login_blueprint.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login_blueprint.login'))

    journal_entries = get_health_journal(user_id)
    user_cookies = request.cookies
    # This will print to the terminal where your Flask app is running
    print("Received cookies:", user_cookies)
    return render_template('dashboard.html', entries=journal_entries)


@login_blueprint.route('/doctor_dashboard')
def doctor_dashboard():
    # Make sure the user is logged in and is a doctor
    if 'user_id' in session and session.get('user_role') == 'doctor':
        # Fetch necessary data for the doctor's dashboard
        return render_template('dashboardDoctor.html')
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login_blueprint.doctor_login'))


@login_blueprint.route('/loginControl', methods=['GET', 'POST'])
def login_control():
    if request.method == 'POST':
        input_code = request.form['code']
        correct_code = session.get('2fa_code', '')

        if input_code == correct_code:
            session.pop('2fa_code', None)
            session.pop('tries', None)
            flash('2FA Verification successful!', 'success')
            # Redirect based on user role
            if session.get('user_role') == 'doctor':
                return redirect(url_for('login_blueprint.doctor_dashboard'))
            else:
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
                if session.get('user_role') == 'doctor':
                    return redirect(url_for('login_blueprint.doctor_login'))
                else:
                    return redirect(url_for('login_blueprint.patient_login'))

    return render_template('loginControl.html')


@login_blueprint.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out.', 'info')
    # Redirect to the homepage
    # Ensure 'home' is correctly defined in your app routes
    return redirect(url_for('home'))


@login_blueprint.route('/loginControl/doctor', methods=['GET', 'POST'])
def login_control_doctor():
    if request.method == 'POST':
        input_code = request.form['code']
        correct_code = session.get('2fa_code', None)

        if input_code == correct_code and session.get('user_role') == 'doctor':
            session.pop('2fa_code', None)
            session.pop('tries', None)
            flash('2FA Verification successful!', 'success')
            # Ensure this route leads to the doctor's dashboard
            return redirect(url_for('login_blueprint.doctor_dashboard'))
        else:
            session['tries'] -= 1
            if session['tries'] > 0:
                flash(f'Invalid 2FA code. {
                      session["tries"]} attempts left.', 'error')
            else:
                session.pop('tries', None)
                session.pop('2fa_code', None)
                flash('You have exceeded the number of attempts.', 'error')
                return redirect(url_for('login_blueprint.doctor_login'))

    # This could be the same as loginControl.html if it adapts dynamically based on the user role
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


@login_blueprint.route('/view-messages', methods=['GET'])
def view_messages():
    # Ensure the doctor is logged in
    if 'doctor_id' not in session:
        return jsonify({'error': 'Not authorized'}), 401

    messages = []
    with open('inquiry.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            messages.append(
                {'username': row['Username'], 'message': row['Message']})
    return jsonify(messages)


@login_blueprint.route('/get-patients', methods=['GET'])
def get_patients():
    # Ensure the doctor is logged in
    if 'doctor_id' not in session:
        return jsonify({'error': 'Not authorized'}), 401

    patients = []
    with open('users.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if {'id': row['ID'], 'username': row['Username']} not in patients:
                patients.append({'id': row['ID'], 'username': row['Username']})
    return jsonify(patients)


@login_blueprint.route('/send-to-patient', methods=['POST'])
def send_to_patient():
    # Ensure the doctor is logged in
    if 'doctor_id' not in session:
        return jsonify({'error': 'Not authorized'}), 401

    data = request.get_json()
    patient_id = data['patientId']
    message = data['message']

    # Append message to health journal or similar action
    with open('healthJournal.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([patient_id, message])

    return jsonify({'success': True})

# Importing necessary Flask components
from flask import Blueprint, request, flash, redirect, url_for, session, render_template
import csv  # Importing CSV module
# Importing two-factor authentication functions
from twoFA import generate_secure_code, send_code_via_email
from hashing import hash_string  # Importing the hash_string function
from salting import salt  # Importing the salt function
# Make sure to import this here  # Importing function to get health journal
from healthJournal import get_health_journal
# Add this import if it's not already there  # Importing jsonify for JSON responses
from flask import jsonify
# Importing functions from lookupSQL
from lookupSQL import username_exists, conn_sql
import psycopg2  # Importing psycopg2 for PostgreSQL interaction

# Creating a Blueprint for login routes
login_blueprint = Blueprint('login_blueprint', __name__)


# Defining function to verify user credentials
def verify_user_credentials(username, hashed_password, user_type='patient'):
    cur, conn = conn_sql()  # Getting SQL connection and cursor

    # Choose the appropriate table based on user type
    # Selecting table name based on user type
    table_name = 'doctors' if user_type == 'doctor' else 'users'

    try:
        # SQL query to find the user with given username and password
        cur.execute(
            "SELECT email, id FROM {} WHERE username = %s AND password = %s".format(
                table_name),
            (username, hashed_password)
        )

        # Fetch the first result
        result = cur.fetchone()  # Fetching one result from the query
        if result:  # Checking if result is not None
            email, user_id = result  # Extracting email and user ID from the result
            # Returning True, email, and user ID if credentials are valid
            return True, email, user_id
        else:
            return False, None, None  # Returning False, None, None if credentials are invalid
    except psycopg2.Error as e:  # Handling database errors
        print(f"An error occurred: {e}")  # Printing the error message
        return False, None, None  # Returning False, None, None in case of an error
    finally:
        if cur:  # Checking if cursor is not None
            cur.close()  # Closing the cursor
        if conn:  # Checking if connection is not None
            conn.close()  # Closing the connection


# Defining route for patient login with GET and POST methods
@login_blueprint.route('/login/patient', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':  # Checking if the request method is POST
        username = request.form['username']  # Retrieving username from form
        password = request.form['password']  # Retrieving password from form
        # Hashing the password with salt
        hashed_password = hash_string(password + salt())
        user_verified, user_email, user_id = verify_user_credentials(
            username, hashed_password, user_type='patient')  # Verifying user credentials

        if user_verified:  # Checking if the user is verified
            session.clear()  # Clear previous session before setting new values
            session['user_id'] = user_id  # Setting session user_id
            session['username'] = username  # Setting session username
            session['email'] = user_email  # Setting session email
            session['user_role'] = 'patient'  # Explicitly set the user role
            code = generate_secure_code()  # Generating secure code for 2FA
            send_code_via_email(user_email, code)  # Sending 2FA code via email
            session['2fa_code'] = code  # Setting session 2FA code
            session['tries'] = 3  # Initialize the number of tries for 2FA
            flash('Login successful. Check your email for the 2FA code.',
                  'info')  # Flashing login success message
            # Redirect to 2FA verification page
            # Redirecting to login control route
            return redirect(url_for('login_blueprint.login_control'))
        else:
            # Flashing invalid credentials message
            flash('Invalid username or password.', 'error')
            # Rendering the patient login template
            return render_template('patientLogin.html')
    else:
        # Rendering the patient login template for GET requests
        return render_template('patientLogin.html')


# Defining route for doctor login with GET and POST methods
@login_blueprint.route('/login/doctor', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':  # Checking if the request method is POST
        username = request.form['username']  # Retrieving username from form
        password = request.form['password']  # Retrieving password from form
        # Hashing the password with salt
        hashed_password = hash_string(password + salt())
        user_verified, user_email, user_id = verify_user_credentials(
            username, hashed_password, user_type='doctor')  # Verifying doctor credentials

        if user_verified:  # Checking if the doctor is verified
            session.clear()  # Clear previous session before setting new values
            session['user_id'] = user_id  # Setting session user_id
            session['username'] = username  # Setting session username
            session['email'] = user_email  # Setting session email
            session['user_role'] = 'doctor'  # Identify the user as a doctor
            code = generate_secure_code()  # Generating secure code for 2FA
            send_code_via_email(user_email, code)  # Sending 2FA code via email
            session['2fa_code'] = code  # Setting session 2FA code
            session['tries'] = 3  # Initialize the number of tries for 2FA
            flash('Login successful. Check your email for the 2FA code.',
                  'info')  # Flashing login success message
            # Redirecting to login control doctor route
            return redirect(url_for('login_blueprint.login_control_doctor'))
        else:
            # Flashing invalid credentials message
            flash('Invalid username or password.', 'error')
            # Rendering the doctor login template
            return render_template('doctorLogin.html')
    else:
        # Rendering the doctor login template for GET requests
        return render_template('doctorLogin.html')


@login_blueprint.route('/dashboard')  # Defining route for dashboard
def dashboard():
    user_id = session.get('user_id')  # Getting user_id from session
    if not user_id:  # Checking if user_id is not in session
        # Flashing login required message
        flash('Please log in to access this page.', 'error')
        # Redirecting to login route
        return redirect(url_for('login_blueprint.login'))

    # Getting health journal entries for the user
    journal_entries = get_health_journal(user_id)
    user_cookies = request.cookies  # Getting cookies from the request
    # This will print to the terminal where your Flask app is running
    print("Received cookies:", user_cookies)  # Printing received cookies
    # Rendering the dashboard template with journal entries
    return render_template('dashboard.html', entries=journal_entries)


# Defining route for doctor dashboard
@login_blueprint.route('/doctor_dashboard')
def doctor_dashboard():
    # Make sure the user is logged in and is a doctor
    # Checking if the user is logged in and is a doctor
    if 'user_id' in session and session.get('user_role') == 'doctor':
        # Fetch necessary data for the doctor's dashboard
        # Rendering the doctor dashboard template
        return render_template('dashboardDoctor.html')
    else:
        # Flashing login required message
        flash('Please log in to access this page.', 'error')
        # Redirecting to doctor login route
        return redirect(url_for('login_blueprint.doctor_login'))


# Defining route for login control with GET and POST methods
@login_blueprint.route('/loginControl', methods=['GET', 'POST'])
def login_control():
    if request.method == 'POST':  # Checking if the request method is POST
        input_code = request.form['code']  # Getting 2FA code from form
        # Getting the correct 2FA code from session
        correct_code = session.get('2fa_code', '')

        if input_code == correct_code:  # Checking if the input code matches the correct code
            session.pop('2fa_code', None)  # Removing 2FA code from session
            session.pop('tries', None)  # Removing tries from session
            # Flashing 2FA success message
            flash('2FA Verification successful!', 'success')
            # Redirect based on user role
            # Checking if the user role is doctor
            if session.get('user_role') == 'doctor':
                # Redirecting to doctor dashboard
                return redirect(url_for('login_blueprint.doctor_dashboard'))
            else:
                # Redirecting to patient dashboard
                return redirect(url_for('login_blueprint.dashboard'))
        else:
            session['tries'] -= 1  # Decrementing the number of tries
            if session['tries'] > 0:  # Checking if there are tries left
                # Flashing invalid 2FA code message
                flash(f'Invalid 2FA code. {
                      session["tries"]} attempts left.', 'error')
            else:
                session.pop('tries', None)  # Removing tries from session
                session.pop('2fa_code', None)  # Removing 2FA

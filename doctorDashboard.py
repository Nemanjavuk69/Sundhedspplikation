# Importing necessary Flask components
from flask import jsonify, Blueprint, render_template, session, flash, redirect, url_for, request
# Importing function to verify doctor credentials
from doctors import verify_doctor_credentials
import csv  # Importing CSV module
from lookupSQL import conn_sql  # Importing SQL connection function
from psycopg2 import sql  # Importing SQL module from psycopg2

# Create a Blueprint for the doctor dashboard
# Creating a Blueprint named 'doctor'
doctor_blueprint = Blueprint('doctor', __name__, template_folder='templates')


@doctor_blueprint.route('/dashboard')  # Defining route for the dashboard
def dashboard():
    # Checking if the user is not logged in as a doctor
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        # Flashing an unauthorized access message
        flash('Unauthorized access.', 'error')
        # Ensure this is correct
        # Redirecting to doctor login page
        return redirect(url_for('doctor.doctor_login'))
    # Rendering the doctor dashboard template
    return render_template('dashboardDoctor.html')


# Defining route for doctor login with GET and POST methods
@doctor_blueprint.route('/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':  # Checking if the request method is POST
        username = request.form['username']  # Retrieving username from form
        password = request.form['password']  # Retrieving password from form
        authenticated, email, doctor_id = verify_doctor_credentials(
            username, password)  # Verifying doctor credentials
        if authenticated:  # Checking if the credentials are authenticated
            session['user_id'] = doctor_id  # Setting session user_id
            # Setting session user_role to doctor
            session['user_role'] = 'doctor'
            session['email'] = email  # Setting session email
            # Redirecting to doctor dashboard
            return redirect(url_for('doctor.dashboard'))
        else:
            # Flashing invalid credentials message
            flash('Invalid username or password.', 'error')
            # Rendering the doctor login template
            return render_template('doctorLogin.html')
    # Rendering the doctor login template for GET requests
    return render_template('doctorLogin.html')


# Defining route to get patient messages
@doctor_blueprint.route('/get-patient-messages')
def get_patient_messages():
    # Checking if the user is not logged in as a doctor
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        # ensure the user is logged in as a doctor
        # Returning unauthorized error
        return jsonify({'error': 'Unauthorized'}), 401

    messages = []  # Initializing messages list
    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor
        # Query to fetch messages
        # SQL query to select messages
        select_query = sql.SQL("SELECT username, message FROM inquries")
        cur.execute(select_query)  # Executing the query

        # Fetch all rows from the executed query
        rows = cur.fetchall()  # Fetching all rows from the query result

        # Process each row and append to the messages list
        for row in rows:  # Iterating through the rows
            # Appending message to the list
            messages.append({'username': row[0], 'message': row[1]})

        # Close the cursor and connection
        cur.close()  # Closing the cursor
        conn.close()  # Closing the connection

        return jsonify(messages)  # Returning the messages as JSON

    except Exception as e:  # Handling exceptions
        # Handle the exception and return an error response
        print(f"Error: {e}")  # Printing the error message
        # Returning error response
        return jsonify({'error': 'An error occurred while fetching patient messages.'}), 500


@doctor_blueprint.route('/get-patients')  # Defining route to get patients
def get_patients():
    # Checking if the user is not logged in as a doctor
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        # Returning unauthorized error
        return jsonify({'error': 'Unauthorized'}), 401

    patients = []  # Initializing patients list
    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor
        # Query to fetch patients
        select_query = sql.SQL(
            "SELECT id, username FROM users WHERE type = %s")  # SQL query to select patients
        # Executing the query with type 'P' (patient)
        cur.execute(select_query, ('P',))

        # Fetch all rows from the executed query
        rows = cur.fetchall()  # Fetching all rows from the query result

        # Process each row and append to the patients list
        for row in rows:  # Iterating through the rows
            # Appending patient to the list
            patients.append({'id': row[0], 'username': row[1]})

        # Close the cursor and connection
        cur.close()  # Closing the cursor
        conn.close()  # Closing the connection

        return jsonify(patients)  # Returning the patients as JSON

    except Exception as e:  # Handling exceptions
        # Handle the exception and return an error response
        print(f"Error: {e}")  # Printing the error message
        # Returning error response
        return jsonify({'error': 'An error occurred while fetching patients.'}), 500


# Defining route to add patient note with POST method
@doctor_blueprint.route('/add-patient-note', methods=['POST'])
def add_patient_note():
    # Checking if the user is not logged in as a doctor
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        # Returning unauthorized error
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()  # Getting JSON data from request
    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor
        # Insert data into the database
        insert_query = sql.SQL(
            # SQL query to insert patient note
            "INSERT INTO journals (userid, entry) VALUES (%s, %s)")
        # Executing the query with userId and entry
        cur.execute(insert_query, (data['userId'], data['entry']))

        # Commit the transaction
        conn.commit()  # Committing the transaction

        # Close the cursor and connection
        cur.close()  # Closing the cursor
        conn.close()  # Closing the connection

        # Return success response
        return jsonify({'success': True})  # Returning success response
    except Exception as e:  # Handling exceptions
        # Handle the exception and return an error response
        print(f"Error: {e}")  # Printing the error message
        # Returning error response
        return jsonify({'error': 'An error occurred while adding the patient note.'}), 500

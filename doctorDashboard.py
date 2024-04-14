from flask import jsonify, Blueprint, render_template, session, flash, redirect, url_for, request
from doctors import verify_doctor_credentials
import csv

# Create a Blueprint for the doctor dashboard
doctor_blueprint = Blueprint('doctor', __name__, template_folder='templates')


@doctor_blueprint.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        flash('Unauthorized access.', 'error')
        # Ensure this is correct
        return redirect(url_for('doctor.doctor_login'))
    return render_template('dashboardDoctor.html')


@doctor_blueprint.route('/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        authenticated, email, doctor_id = verify_doctor_credentials(
            username, password)
        if authenticated:
            session['user_id'] = doctor_id
            session['user_role'] = 'doctor'
            session['email'] = email
            return redirect(url_for('doctor.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('doctorLogin.html')
    return render_template('doctorLogin.html')


@doctor_blueprint.route('/get-patient-messages')
def get_patient_messages():
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        # ensure the user is logged in as a doctor
        return jsonify({'error': 'Unauthorized'}), 401

    messages = []
    with open('inquiry.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            messages.append(
                {'username': row['Username'], 'message': row['Message']})
    return jsonify(messages)


@doctor_blueprint.route('/get-patients')
def get_patients():
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401

    patients = []
    with open('users.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type'] == 'P':  # Ensure only patients are included
                patients.append({'id': row['ID'], 'username': row['Username']})
    return jsonify(patients)


@doctor_blueprint.route('/add-patient-note', methods=['POST'])
def add_patient_note():
    if 'user_id' not in session or session.get('user_role') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    with open('healthJournal.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data['userId'], data['entry']])
    return jsonify({'success': True})

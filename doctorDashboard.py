from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from doctors import verify_doctor_credentials

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

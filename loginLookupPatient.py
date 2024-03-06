# loginLookup.py
from flask import Blueprint, request, flash, redirect, url_for
import csv
from hashing import hash_string

login_lookup_patient = Blueprint('login_lookup_patient', __name__)


@login_lookup_patient.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform login lookup in your database
        # For example:
        username = request.form['username']
        password = request.form['password']

        hashedPassword = hash_string(password)
        # Logic to verify username and password
        # Replace 'example.csv' with the path to your actual CSV file
        users = 'users.csv'

        found_user = False
        with open(users, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                # Assuming username is in the first column, password in the second
                if username == row[0] and hashedPassword == row[1]:
                    found_user = True
                    break

        if found_user:
            flash('Login successful.')
            # Make sure this points to the correct view function
            return redirect(url_for('yay'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('sad'))  # Adjust as necessary

        flash('Login successful.')
        return redirect(url_for('home'))
    return 'Login Page'

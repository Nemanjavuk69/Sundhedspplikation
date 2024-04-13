from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import csv
from hashing import hash_string
from salting import salt
import os
from time import time
import pandas as pd

register_user = Blueprint('register_user', __name__,
                          template_folder='templates')


def username_exists(username):
    with open('users.csv', mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower() == username.lower():
                return True
    return False


@register_user.route('/register', methods=['GET', 'POST'])
def register():
    file_path_U = 'users.csv'
    file_path_P = 'doctors.csv'
    df = pd.read_csv(file_path_U)
    ID = len(df)
    if request.method == 'POST':
        # Check if we already processed this form submission
        form_token = request.form.get('form_token')
        if session.get('last_form_token') == form_token:
            # Ignore resubmission
            return redirect(url_for('register_user.register'))
        # Store the token in the session
        session['last_form_token'] = form_token

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        type = request.form['type']

        if username_exists(username):
            flash('The username is already in use',
                  'registration_error')  # Flash message
            return redirect(url_for('register_user.register'))

        hashed_password = hash_string(password+salt())
        if type == 'P':
            with open(file_path_U, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([username, hashed_password, email, ID, type])
            flash('Registration successful! Please login.',
                  'registration_success')
            return redirect(url_for('register_user.register'))

        elif type == 'H':
            with open(file_path_P, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([username, hashed_password, email, ID, type])
            flash('Registration successful! Please login.',
                  'registration_success')
            return redirect(url_for('register_user.register'))
    # Generate a unique token for the form
    form_token = os.urandom(12).hex()
    session['last_form_token'] = form_token
    return render_template('registerUser.html', form_token=form_token, cache_buster=int(time()))

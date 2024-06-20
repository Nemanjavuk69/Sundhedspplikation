# Importing necessary Flask components
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import csv  # Importing CSV module
from hashing import hash_string  # Importing hash_string function
from salting import salt  # Importing salt function
import os  # Importing os module
from time import time  # Importing time function
import pandas as pd  # Importing pandas module
# Importing postgreSQL_con function from insertSQL
from insertSQL import postgreSQL_con
# Importing functions from lookupSQL
from lookupSQL import username_exists, email_exists
# Importing validation functions
from registerRequirements import is_strong_password, is_valid_password, is_valid_email

# Creating a Blueprint for user registration
register_user = Blueprint('register_user', __name__,
                          template_folder='templates')


# Defining route for registration with GET and POST methods
@register_user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Checking if the request method is POST
        # Check if we already processed this form submission
        # Retrieving form token from the request
        form_token = request.form.get('form_token')
        # Checking if the form token matches the last form token in session
        if session.get('last_form_token') == form_token:
            # Ignore resubmission
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))
        # Store the token in the session
        # Storing the form token in the session
        session['last_form_token'] = form_token

        # Retrieving username from the form
        username = request.form['username']
        # Retrieving password from the form
        password = request.form['password']
        email = request.form['email']  # Retrieving email from the form
        type = request.form['type']  # Retrieving user type from the form

        if username_exists(username):  # Checking if the username already exists
            flash('The username is already in use',
                  'registration_error')  # Flash message
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

        if email_exists(email):  # Checking if the email already exists
            flash('The email is already in use',
                  'registration_error')  # Flash message
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

        if is_valid_email(email) == False:  # Checking if the email is valid
            flash('The email is not a recognized email, try with another one.',
                  'registration_error')  # Flash message
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

        # Checking if the password is valid
        if is_valid_password(password) == False:
            flash('The password must be between 8 and 16 characters long',
                  'registration_error')  # Flash message
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

        # Checking if the password is strong
        if is_strong_password(password) == False:
            flash('The password is not strong enough. '
                  'Password need at least one special character. '
                  'The password must not contain three consecutive digits. '
                  # Flash message
                  'The password must include at least one uppercase letter.', 'registration_error')
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

        # Hashing the password with salt
        hashed_password = hash_string(password + salt())
        if type == 'P':  # Checking if the user type is 'P'
            # Inserting user into the database
            postgreSQL_con(username, hashed_password, email, type)
            flash('Registration successful! Please login.',
                  'registration_success')  # Flash message
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

        elif type == 'H':  # Checking if the user type is 'H'
            # Inserting user into the database
            postgreSQL_con(username, hashed_password, email, type)
            flash('Registration successful! Please login.',
                  'registration_success')  # Flash message
            # Redirecting to the registration page
            return redirect(url_for('register_user.register'))

    # Generate a unique token for the form
    form_token = os.urandom(12).hex()  # Generating a unique form token
    # Storing the form token in the session
    session['last_form_token'] = form_token
    # Rendering the registration template with form token and cache buster
    return render_template('registerUser.html', form_token=form_token, cache_buster=int(time()))

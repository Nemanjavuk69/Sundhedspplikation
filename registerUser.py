from flask import Blueprint, request, render_template, redirect, url_for, flash
import csv
from hashing import hash_string

# Create a Flask Blueprint named 'register_user'
register_user = Blueprint('register_user', __name__,
                          template_folder='templates')

# Check if the username already exists in the CSV file


def username_exists(username):
    with open('users.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == username:
                return True
    return False


@register_user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username_exists(username):
            # If the username already exists, inform the user
            flash('Username already in use')
            return redirect(url_for('register_user.register'))
        else:
            # Hash the password and save the new user to the CSV file
            hashed_password = hash_string(password)
            with open('users.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([username, hashed_password])
            flash('Registration successful! Please login.')
            return redirect(url_for('register_user.register'))

    return render_template('registerUser.html')

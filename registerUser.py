from flask import Blueprint, request, render_template, redirect, url_for, flash
import csv
from hashing import hash_string
from salting import salt

register_user = Blueprint('register_user', __name__,
                          template_folder='templates')


def username_exists(username):
    with open('users.csv', mode='r', newline='') as csvfile:
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
            flash('The username is already in use', 'error')  # Flash message
            return redirect(url_for('register_user.register'))

        hashed_password = hash_string(password+salt())
        with open('users.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, hashed_password])
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('register_user.register'))

    return render_template('registerUser.html')

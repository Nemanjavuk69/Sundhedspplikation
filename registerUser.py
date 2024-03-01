# registerUser.py
from flask import Blueprint, request, flash, redirect, url_for

register_user = Blueprint('register_user', __name__)


@register_user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Perform user registration, add user to your database
        # For example:
        username = request.form['username']
        password = request.form['password']
        # Logic to add user to the database
        flash('Registration successful.')
        return redirect(url_for('index'))
    return 'Registration Page'

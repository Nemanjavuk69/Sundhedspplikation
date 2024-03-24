from flask import Flask, render_template, request, flash, redirect, url_for, session
from loginLookup import login_blueprint
from registerUser import register_user
from twoFA import generate_secure_code, send_code_via_email


app = Flask(__name__)
app.secret_key = '123456'

# Register the blueprints
app.register_blueprint(login_blueprint, url_prefix='/auth')
app.register_blueprint(register_user, url_prefix='/auth')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Something
        pass
    return render_template('index.html')


# @app.errorhandler(404)
# def page_not_found(e):
#    # Your 404 page logic
#    return '404 Not Found', 404


@app.route('/sad', methods=['GET', 'POST'])
def sad():
    if request.method == 'POST':
        # Handle healthcare personnel login form submission here
        pass
    return render_template('sad.html')


@app.route('/yay', methods=['GET'])
def yay():
    # This route simply displays the 'yay.html' page
    return render_template('yay.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verify login credentials and get user email
        success, user_email = login(username, password)
        if success:
            code = generate_secure_code()
            send_code_via_email(user_email, code)
            session['2fa_code'] = code
            flash('Login successful. Check your email for the 2FA code.', 'info')
            # Corrected redirect below
            return redirect(url_for('login_blueprint.login_control'))
        else:
            flash('Invalid username or password.', 'error')
            # Make sure any other redirect also uses the correct Blueprint name
            return redirect(url_for('login_blueprint.login_page'))
    # Reload the login page on GET or failed login
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register():
    # Render the registration form template
    return render_template('registerUser.html')


if __name__ == '__main__':
    app.run(debug=True)

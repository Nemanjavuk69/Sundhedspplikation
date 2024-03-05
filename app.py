from flask import Flask, render_template, request, flash, redirect, url_for
from loginLookup import login_lookup
from registerUser import register_user

app = Flask(__name__)
app.secret_key = '123456'

# Register the blueprints
app.register_blueprint(login_lookup, url_prefix='/auth')
app.register_blueprint(register_user, url_prefix='/auth')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_login = request.form['username']
        if user_login == "Admin":
            print("!!!CONGRATULATIONS!!!")
            flash("!!!CONGRATULATIONS!!! You are logged in as Admin.")
            return render_template('index.html')
        else:
            flash("Invalid login. Please try again.")
    return render_template('index.html')


@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        # Handle patient login form submission here
        pass
    return render_template('patient-login.html')


@app.route('/healthcare-login', methods=['GET', 'POST'])
def healthcare_login():
    if request.method == 'POST':
        # Handle healthcare personnel login form submission here
        pass
    return render_template('healthcare-login.html')


@app.route('/sad', methods=['GET', 'POST'])
def sad():
    if request.method == 'POST':
        # Handle healthcare personnel login form submission here
        pass
    return render_template('sad.html')


@app.route('/yay', methods=['GET', 'POST'])
def yay():
    if request.method == 'POST':
        # Handle healthcare personnel login form submission here
        pass
    return render_template('yay.html')


if __name__ == '__main__':
    app.run(debug=True)

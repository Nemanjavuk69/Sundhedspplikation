from flask import Flask, render_template, request, flash, redirect, url_for
from loginLookupPatient import login_lookup_patient
from loginLookupHealthcare import login_lookup_healthcare
from registerUser import register_user

app = Flask(__name__)
app.secret_key = '123456'

# Register the blueprints
app.register_blueprint(login_lookup_patient, url_prefix='/auth')
app.register_blueprint(login_lookup_healthcare, url_prefix='/auth')
app.register_blueprint(register_user, url_prefix='/auth')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Something
        pass
    return render_template('index.html')


@app.route('/patientLogin', methods=['GET', 'POST'])
def patientLogin():
    if request.method == 'POST':
        # Handle patient login form submission here
        pass
    return render_template('patientLogin.html')


@app.route('/healthcareLogin', methods=['GET', 'POST'])
def healthcareLogin():
    if request.method == 'POST':
        # Handle healthcare personnel login form submission here
        pass
    return render_template('healthcareLogin.html')


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


@app.route('/login-options')
def login_options():
    # Assuming you have a file named 'loginOptions.html' in the 'templates' directory
    return render_template('loginOptions.html')


@app.route('/register', methods=['GET'])
def register():
    # Render the registration form template
    return render_template('registerUser.html')


if __name__ == '__main__':
    app.run(debug=True)

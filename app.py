from flask import Flask, render_template, request, flash, redirect, url_for, session
from loginLookup import login_blueprint
from registerUser import register_user
from twoFA import generate_secure_code, send_code_via_email
from healthJournal import get_health_journal
from doctorDashboard import doctor_blueprint
from loginLookup import verify_user_credentials

app = Flask(__name__)
app.secret_key = '123456'

# Register the blueprints
app.register_blueprint(login_blueprint, url_prefix='/auth')
app.register_blueprint(register_user, url_prefix='/auth')
# Register the doctor blueprint
app.register_blueprint(doctor_blueprint, url_prefix='/doctor')


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


@app.route('/register', methods=['GET'])
def register():
    # Render the registration form template
    return render_template('registerUser.html')


if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)

# Importing necessary Flask components
from flask import Flask, render_template, request, flash, redirect, url_for, session
# Importing the login blueprint from loginLookup
from loginLookup import login_blueprint
# Importing the register_user function from registerUser
from registerUser import register_user
# Importing two-factor authentication functions
from twoFA import generate_secure_code, send_code_via_email
# Importing function to get health journal
from healthJournal import get_health_journal
# Importing the doctor blueprint from doctorDashboard
from doctorDashboard import doctor_blueprint
# Importing user credentials verification function
from loginLookup import verify_user_credentials

app = Flask(__name__)  # Creating an instance of the Flask class
# Setting a secret key for the Flask app (used for session management, etc.)
app.secret_key = '123456'

# Register the blueprints
# Registering the login blueprint with URL prefix '/auth'
app.register_blueprint(login_blueprint, url_prefix='/auth')
# Registering the register_user blueprint with URL prefix '/auth'
app.register_blueprint(register_user, url_prefix='/auth')
# Register the doctor blueprint
# Registering the doctor blueprint with URL prefix '/doctor'
app.register_blueprint(doctor_blueprint, url_prefix='/doctor')


# Defining the home route with GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':  # Checking if the request method is POST
        # Something
        pass  # Placeholder for POST request handling logic
    # Rendering the 'index.html' template for GET requests
    return render_template('index.html')

# @app.errorhandler(404)
# def page_not_found(e):
#    # Your 404 page logic
#    return '404 Not Found', 404


# Defining the sad route with GET and POST methods
@app.route('/sad', methods=['GET', 'POST'])
def sad():
    if request.method == 'POST':  # Checking if the request method is POST
        # Handle healthcare personnel login form submission here
        pass  # Placeholder for POST request handling logic
    # Rendering the 'sad.html' template for GET requests
    return render_template('sad.html')


@app.route('/yay', methods=['GET'])  # Defining the yay route with GET method
def yay():
    # This route simply displays the 'yay.html' page
    return render_template('yay.html')  # Rendering the 'yay.html' template


# Defining the register route with GET method
@app.route('/register', methods=['GET'])
def register():
    # Render the registration form template
    # Rendering the 'registerUser.html' template
    return render_template('registerUser.html')


if __name__ == '__main__':  # Ensuring this block runs only if the script is executed directly
    # SSL context with certificate and key files
    context = ('cert.pem', 'key.pem')
    # Running the Flask app on port 443 with SSL context
    app.run(host='0.0.0.0', port=443, ssl_context=context)

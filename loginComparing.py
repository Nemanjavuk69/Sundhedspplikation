from flask import Flask, render_template, request, flash

app = Flask(__name__)
# Replace 'your_secret_key' with a real key for flashing messages
app.secret_key = '123456'


@app.route('/', methods=['GET', 'POST'])  # Allow both GET and POST requests
def home():
    if request.method == 'POST':
        # Get the username from the form
        user_login = request.form['username']
        # Compare it with your 'Admin' username
        if user_login == "Admin":
            # If it's a match, print a message to the console (server side)
            print("!!!CONGRATULATIONS!!!")
            # You might want to flash a message to the user as well
            flash("!!!CONGRATULATIONS!!! You are logged in as Admin.")
            # Redirect or render a template as necessary
            # return redirect(url_for('admin_dashboard'))
            # or
            return render_template('index.html')
        else:
            # Flash message for an invalid login
            flash("Invalid login. Please try again.")
    # Render the login page template on GET request
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

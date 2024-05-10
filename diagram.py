from graphviz import Digraph

# Create a new Digraph (directed graph)
dot = Digraph()

# Add nodes (representing Python files)
# Typically the main entry point of the application. Initializes and configures the application.
dot.node('A', 'App.py')
# Manages the doctor's dashboard interface, likely fetching and displaying patient data.
dot.node('B', 'doctorDashboard.py')
dot.node('C', 'doctors.py')
dot.node('D', 'hashing.py')
dot.node('E', 'healthJournal.py')
dot.node('F', 'loginLookup.py')
dot.node('G', 'registerUser.py')
dot.node('H', 'salting.py')
dot.node('I', 'twoFA.py')

dot.node('HH', 'salting.py')
dot.node('DD', 'hashing.py')


# Add nodes (representing HTML files)
dot.node('J', 'dashboard.html')
dot.node('K', 'dashboardDoctor.html')
dot.node('L', 'doctorLogin.html')
dot.node('M', 'index.html')
dot.node('N', 'loginControl.html')
dot.node('O', 'patientLogin.html')
dot.node('P', 'registerUser.html')


# Add nodes (representing HTML files)
dot.node('Q', 'doctorSettings.js')
dot.node('R', 'userSettings.js')


# Add nodes (representing csv files)
dot.node('S', 'doctors.csv')
dot.node('T', 'healthJournal.csv')
dot.node('U', 'inquiry.csv')
dot.node('V', 'users.csv')


# Add edges (representing interactions)
dot.edge('A', 'M', label='Initializing')

dot.edge('M', 'L', label='Login as healthcare')
dot.edge('M', 'O', label='Login as patient')
dot.edge('M', 'P', label='Register user')

dot.edge('P', 'G', label='ADD user to the database')

dot.edge('HH', 'DD', label='Add salting to POST data')

dot.edge('DD', 'G', label='Convert to Hash')

dot.edge('G', 'V', label='If user is a patient')
dot.edge('G', 'S', label='If user is a healthcare')

dot.edge('L', 'F', label='Import POST data from HTML')

dot.edge('O', 'F', label='Import POST data from HTML')

dot.edge('H', 'D', label='Add salting to POST data')
dot.edge('D', 'F', label='Convert to Hash')

dot.edge('F', 'V', label='If user is a patient')
dot.edge('F', 'S', label='If user is a healthcare')

dot.edge('V', 'M', label='If patient is not found')
dot.edge('V', 'I', label='If patient is found')

dot.edge('S', 'M', label='If healthcare is not found')
dot.edge('S', 'I', label='If healthcare is found')

dot.edge('I', 'N', label='Ask user for 2FA')

dot.edge('N', 'M', label='If 2FA is wrong')
dot.edge('N', 'J', label='If 2FA is correct and user is patient')
dot.edge('N', 'C', label='If 2FA is correct and user is healthcare')

dot.edge('J', 'E', label='Show the individual health journal')

dot.edge('E', 'T', label='Read the patients medical history')

dot.edge('T', 'R', label='Fill the dashboard with patient history')

dot.edge('R', 'J', label='Present the patients health jornal on the Dashboard')

dot.edge('C', 'K', label='Get the individual ID of the healthcare')

dot.edge('K', 'B', label='FETCH master data from patients')

dot.edge('B', 'U', label='Read all patients inquries')

dot.edge('U', 'Q', label='Fill the dashboard with patient data')

dot.edge('Q', 'K', label='Present the patients inquries on the Dashboard')

# Save the DOT source code to a filestamdata
dot.render('function_interactions', format='png', cleanup=True)

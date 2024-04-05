from graphviz import Digraph

# Create a new Digraph (directed graph)
dot = Digraph()

# Add nodes (representing Python files)
dot.node('A', 'App.py')
dot.node('B', 'hashing.py')
dot.node('C', 'loginLookup.py')
dot.node('D', 'registerUser.py')
dot.node('E', 'salting.py')
dot.node('F', 'twoFA.py')
dot.node('G', 'users.csv')

# Add nodes (representing HTML files)
dot.node('H', 'index.html')
dot.node('I', 'login.html')
dot.node('J', 'loginControl.html')
dot.node('K', 'registerUser.html')
dot.node('L', 'sad.html')
dot.node('M', 'yay.html')

# Add edges (representing interactions)
dot.edge('A', 'H', label='Initializing')
dot.edge('H', 'I', label='Login')
dot.edge('H', 'K', label='Register')
dot.edge('K', 'D', label='Registering user')
dot.edge('D', 'G', label='Add user to database')
dot.edge('I', 'C', label='Import POST data from HTML')


dot.edge('C', 'G', label='Check')
dot.edge('G', 'J', label='If user found')
dot.edge('J', 'F', label='Send 2FA to user')
dot.edge('F', 'L', label='If 2FA failed')
dot.edge('F', 'M', label='If 2FA succeed')
dot.edge('G', 'L', label='else user not found')

dot.edge('B', 'C', label='Hash the POST data')
dot.edge('C', 'B', label='Convert to Hash')
dot.edge('E', 'B', label='Add salting to POST data')

# Save the DOT source code to a file
dot.render('function_interactions', format='png', cleanup=True)

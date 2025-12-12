from graphviz import Digraph

dot = Digraph(comment='Nobel Prize Laureates Autocomplete Application')

# Set graph attributes
dot.attr(rankdir='TB', layout='dot')

# Front-end components
dot.node('FE', 'Front-end')
dot.node('HTML', 'index.html')
dot.node('CSS', 'main.css')
dot.node('JS', 'main.js')

# Back-end components
dot.node('BE', 'Back-end')
dot.node('Server', 'server.js')
dot.node('Router', 'router.js')
dot.node('Handler', 'handler.js')
dot.node('Algorithm', 'algorithm.js')
dot.node('Data', 'data.json')

# Testing components
dot.node('Test', 'Testing')
dot.node('QUnit', 'qunit.html')
dot.node('FETest', 'frontendTests.js')
dot.node('BETest', 'backendTests.js')

# Documentation
dot.node('Doc', 'Documentation')
dot.node('ReadMe', 'README.md')

# Define edges for communication and interactions
dot.edges([('FE', 'BE'), ('FE', 'HTML'), ('FE', 'CSS'), ('FE', 'JS')])
dot.edges([('BE', 'Server'), ('BE', 'Router'), ('BE', 'Handler'), ('BE', 'Algorithm'), ('BE', 'Data')])
dot.edges([('Test', 'QUnit'), ('Test', 'FETest'), ('Test', 'BETest')])
dot.edge('Doc', 'ReadMe')

# Connect front-end to back-end via REST API
dot.edge('JS', 'Server', label='REST API', style='dotted')

# Connect server components
dot.edge('Server', 'Router')
dot.edge('Router', 'Handler')
dot.edge('Handler', 'Algorithm')
dot.edge('Algorithm', 'Data')

# Visualize the graph
dot.render(filename='nobel_prize_autocomplete_architecture', format='png', cleanup=True)
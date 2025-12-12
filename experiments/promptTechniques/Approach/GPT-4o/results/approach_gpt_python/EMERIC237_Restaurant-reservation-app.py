from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Restaurant Reservation Application Architecture')

# Set graph attributes
dot.attr(rankdir='LR', size='10,5')

# Add nodes for main components
dot.node('FE', 'Frontend (React)', shape='rect', style='filled', fillcolor='lightblue')
dot.node('BE', 'Backend (Node.js/Express)', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('DB', 'Database (PostgreSQL)', shape='rect', style='filled', fillcolor='lightyellow')

# Add nodes for backend subcomponents
dot.node('API', 'RESTful API', shape='rect', style='dotted')
dot.node('Router', 'Router', shape='rect')
dot.node('Controller', 'Controller', shape='rect')
dot.node('Service', 'Service', shape='rect')
dot.node('Knex', 'Knex (Query Builder)', shape='rect')

# Add edges for frontend-backend communication
dot.edge('FE', 'API', 'HTTP Requests (REST)')

# Add edges for backend internal communication
dot.edge('API', 'Router', 'Route Handling')
dot.edge('Router', 'Controller', 'Forward Requests')
dot.edge('Controller', 'Service', 'Business Logic')
dot.edge('Service', 'Knex', 'Database Queries')
dot.edge('Knex', 'DB', 'SQL Queries')

# Add a legend
dot.node('Legend', 'Legend', shape='rect', style='filled', fillcolor='lightgrey')
dot.edge('Legend', 'FE', 'User Interface')
dot.edge('Legend', 'API', 'REST API')
dot.edge('Legend', 'DB', 'Data Storage')

# Render and view the diagram
dot.render('restaurant_reservation_app_architecture', format='png', cleanup=True)
dot.view()
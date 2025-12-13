from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Employee Management System: Microservices Architecture Overview')

# Define node styles
node_style = {
    'shape': 'box',
    'style': 'filled',
    'fillcolor': 'lightgrey'
}

# Define edge styles
edge_style = {
    'arrowhead': 'open'
}

# Subsystems
dot.node('Frontend', 'Frontend (ReactJS)', **node_style)
dot.node('Gateway', 'API Gateway (Spring Boot)', **node_style)
dot.node('Nginx', 'Webserver (Nginx)', **node_style)

# Microservices
dot.node('Attendance', 'Attendance Service (Golang)', **node_style)
dot.node('Employee', 'Employee Service (Golang)', **node_style)
dot.node('Salary', 'Salary Service (Golang)', **node_style)
dot.node('Notification', 'Notification Service (Python)', **node_style)

# Databases
dot.node('MySQL', 'MySQL Database', shape='cylinder', style='filled', fillcolor='lightblue')
dot.node('Elasticsearch', 'Elasticsearch', shape='cylinder', style='filled', fillcolor='lightblue')

# Edges for data flow
dot.edge('Frontend', 'Gateway', label='HTTP Requests', **edge_style)
dot.edge('Gateway', 'Attendance', label='REST API', **edge_style)
dot.edge('Gateway', 'Employee', label='REST API', **edge_style)
dot.edge('Gateway', 'Salary', label='REST API', **edge_style)
dot.edge('Gateway', 'Notification', label='REST API', **edge_style)
dot.edge('Gateway', 'Frontend', label='HTTP Responses', **edge_style)

# Database interactions
dot.edge('Attendance', 'MySQL', label='SQL Queries', **edge_style)
dot.edge('Employee', 'MySQL', label='SQL Queries', **edge_style)
dot.edge('Salary', 'MySQL', label='SQL Queries', **edge_style)
dot.edge('Notification', 'Elasticsearch', label='Search Queries', **edge_style)

# Internal communication
dot.edge('Notification', 'Employee', label='Fetch Employee Data', **edge_style)

# Reverse proxy
dot.edge('Nginx', 'Frontend', label='Serve Frontend', **edge_style)

# Render the digraph to a file
dot.render('employee_management_system_architecture', format='png', cleanup=True)
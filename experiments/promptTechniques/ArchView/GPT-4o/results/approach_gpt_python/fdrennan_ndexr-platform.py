from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Microservice Architecture for Data Pipeline')

# Define node attributes
node_attrs = {'shape': 'rect', 'style': 'filled', 'color': 'lightblue'}

# Add nodes for the main components
dot.node('Reddit', 'Reddit (Data Source)', **node_attrs)
dot.node('PRAW', 'PRAW Library', **node_attrs)
dot.node('PostgreSQL', 'PostgreSQL Database', **node_attrs)
dot.node('R_API', 'R Plumber API', **node_attrs)
dot.node('Shiny', 'Shiny Application', **node_attrs)
dot.node('Airflow', 'Airflow', **node_attrs)
dot.node('AWS', 'AWS Services (S3, EC2, SNS)', **node_attrs)
dot.node('Elasticsearch', 'Elasticsearch', **node_attrs)
dot.node('Glances', 'Glances (System Monitoring)', **node_attrs)
dot.node('Docker', 'Docker Containers', **node_attrs)
dot.node('Nginx', 'NGINX (Load Balancer)', **node_attrs)

# Add edges to represent dependencies and interactions
dot.edge('Reddit', 'PRAW', label='Data Ingestion', dir='forward')
dot.edge('PRAW', 'PostgreSQL', label='Store Data', dir='forward')
dot.edge('PostgreSQL', 'R_API', label='Data Access', dir='forward')
dot.edge('R_API', 'Shiny', label='UI Interaction', dir='forward')
dot.edge('Airflow', 'PRAW', label='Orchestrate', dir='forward')
dot.edge('Airflow', 'AWS', label='Manage Infrastructure', dir='forward')
dot.edge('AWS', 'Elasticsearch', label='Enable Search', dir='forward')
dot.edge('Glances', 'AWS', label='Monitor', dir='forward')
dot.edge('Docker', 'R_API', label='Containerized Deployment', dir='forward')
dot.edge('Docker', 'Shiny', label='Containerized Deployment', dir='forward')
dot.edge('Nginx', 'R_API', label='Load Balancing', dir='forward')

# Render the diagram to a file
dot.render('microservice_architecture_diagram', format='png', cleanup=True)
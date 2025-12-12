from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='DORA Metrics Automation Tool Architecture')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')

# Define node styles
node_style = {'shape': 'rectangle', 'style': 'filled', 'color': 'lightgray'}
service_style = {'shape': 'rectangle', 'style': 'filled', 'color': 'lightblue'}
db_style = {'shape': 'cylinder', 'style': 'filled', 'color': 'lightyellow'}

# Add nodes for services
dot.node('BackendAPI', 'Backend API (Gin-Gonic)', **service_style)
dot.node('GitLabConnector', 'GitLab Connector', **service_style)
dot.node('PrometheusConnector', 'Prometheus Connector', **service_style)
dot.node('MongoDBService', 'MongoDB Service', **service_style)
dot.node('MetricsCalculation', 'Metrics Calculation Services', **service_style)

# Add node for data persistence
dot.node('MongoDB', 'MongoDB', **db_style)

# Add nodes for external systems
dot.node('GitLab', 'GitLab', shape='rectangle', style='filled', color='lightgreen')
dot.node('Prometheus', 'Prometheus', shape='rectangle', style='filled', color='lightgreen')

# Add edges for control flow
dot.edge('BackendAPI', 'GitLabConnector', label='Fetches Data', style='dashed')
dot.edge('GitLabConnector', 'GitLab', label='API Calls', style='dashed')
dot.edge('BackendAPI', 'PrometheusConnector', label='Queries Alerts', style='dashed')
dot.edge('PrometheusConnector', 'Prometheus', label='API Calls', style='dashed')
dot.edge('BackendAPI', 'MongoDBService', label='Stores & Retrieves Data', style='dashed')
dot.edge('MongoDBService', 'MongoDB', label='CRUD Operations', style='dashed')
dot.edge('BackendAPI', 'MetricsCalculation', label='Calculates Metrics', style='dashed')

# Add legend
dot.node('Legend', 'Legend:\nRectangles: Services\nCylinders: Databases\nGreen: External Systems', shape='note')

# Render the graph
dot.render('dora_metrics_architecture', format='png', cleanup=True)
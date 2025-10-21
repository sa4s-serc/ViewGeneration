from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Tiramisu3-PR Public Transportation System')

# Define the styles for the nodes and edges
node_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': '#lightgray'}
db_node_style = {'shape': 'cylinder', 'style': 'filled', 'fillcolor': '#lightblue'}
edge_style = {'arrowhead': 'open'}

# Add nodes for each layer and component
dot.node('Mobile Client', **node_style)
dot.node('Java Frontend', **node_style)
dot.node('Backend Data Processing', **node_style)
dot.node('Python Prediction', **node_style)
dot.node('AWS Infrastructure', **node_style)

# Add nodes for DBs
dot.node('DynamoDB', **db_node_style)
dot.node('PostgresDB', **db_node_style)

# Add edges for communication
dot.edge('Mobile Client', 'Java Frontend', label='REST API', **edge_style)
dot.edge('Java Frontend', 'Backend Data Processing', label='REST API', **edge_style)
dot.edge('Backend Data Processing', 'DynamoDB', label='Data Storage', **edge_style)
dot.edge('Java Frontend', 'PostgresDB', label='User Interaction Logs', **edge_style)
dot.edge('Python Prediction', 'Backend Data Processing', label='Data Analysis', **edge_style)
dot.edge('AWS Infrastructure', 'Backend Data Processing', label='SQS', **edge_style)

# Add additional connectors
dot.edge('Mobile Client', 'AWS Infrastructure', label='Push Notifications', **edge_style)
dot.edge('Python Prediction', 'AWS Infrastructure', label='Route Prediction', **edge_style)

# Add a legend for clarity
with dot.subgraph(name='cluster_legend') as c:
    c.attr(label='Legend')
    c.node('Component', **node_style)
    c.node('Database', **db_node_style)
    c.edge('Component', 'Database', label='Communication', **edge_style)

# Render the graph to a file
dot.render('tiramisu3_pr_architecture', format='png', cleanup=True)
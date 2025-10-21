from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Fintan Case Studies Architecture')

# Define node attributes
node_attrs = {
    'shape': 'box',
    'style': 'filled',
    'fillcolor': 'lightgrey',
    'fontname': 'Helvetica'
}

# Define edge attributes
edge_attrs = {
    'style': 'solid',
    'color': 'black',
    'fontname': 'Helvetica'
}

# Add nodes for key components
dot.node('FR', 'Front-end (React & Redux)', **node_attrs)
dot.node('SS', 'Server-side (Spring Boot)', **node_attrs)
dot.node('NM', 'Native Mobile (React Native)', **node_attrs)
dot.node('DA', 'Desktop App (Electron)', **node_attrs)
dot.node('CI', 'CI/CD Pipeline (Azure DevOps/CircleCI)', **node_attrs)
dot.node('T', 'Automated Testing', **node_attrs)
dot.node('GR', 'gRPC Push Notifications', **node_attrs)
dot.node('MQ', 'Message Queues (ZeroMQ)', **node_attrs)
dot.node('M', 'Monitoring (New Relic)', **node_attrs)
dot.node('L', 'Logging (Elastic Stack)', **node_attrs)
dot.node('S', 'Security (Spring Security & OAuth)', **node_attrs)
dot.node('PM', 'Project Management (ADR)', **node_attrs)

# Add edges for interactions
dot.edge('FR', 'SS', label='API Calls', **edge_attrs)
dot.edge('NM', 'SS', label='API Calls', **edge_attrs)
dot.edge('DA', 'SS', label='API Calls', **edge_attrs)
dot.edge('CI', 'SS', label='Deployments', **edge_attrs)
dot.edge('T', 'SS', label='Tests', **edge_attrs)
dot.edge('GR', 'SS', label='Notifications', **edge_attrs)
dot.edge('MQ', 'SS', label='Message Passing', **edge_attrs)
dot.edge('M', 'SS', label='Monitoring Data', **edge_attrs)
dot.edge('L', 'SS', label='Log Data', **edge_attrs)
dot.edge('S', 'SS', label='Auth & Authz', **edge_attrs)
dot.edge('PM', 'SS', label='Decisions', **edge_attrs)

# Render the diagram
dot.render('fintan_architecture', format='png', cleanup=True)
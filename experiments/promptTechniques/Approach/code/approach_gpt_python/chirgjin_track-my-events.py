from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Event Tracking System Architecture')

# Set graph attributes
dot.attr(rankdir='LR', size='8,5')

# Add nodes for each service and component
dot.node('FR', 'Frontend (React)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('GW', 'Gateway Service', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('TR', 'Tracking Service', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('US', 'User Service', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('DBP', 'PostgreSQL', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('DBR', 'Redis', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('SDK', 'JavaScript SDK', shape='ellipse', style='filled', fillcolor='lightpink')

# Add edges for communication
dot.edge('FR', 'GW', label='REST API', style='dashed')
dot.edge('GW', 'TR', label='REST API & Auth', style='dashed')
dot.edge('GW', 'US', label='REST API & Auth', style='dashed')
dot.edge('TR', 'DBP', label='Store Events', style='dashed')
dot.edge('US', 'DBP', label='Store User Data', style='dashed')
dot.edge('SDK', 'TR', label='Event Data', style='dashed')
dot.edge('TR', 'DBR', label='Pub/Sub Events', style='dashed')
dot.edge('GW', 'DBR', label='Subscribe', style='dashed')

# Add cluster for frontend components
with dot.subgraph(name='cluster_frontend') as c:
    c.attr(label='Frontend Components')
    c.node('C1', 'Chart', shape='ellipse')
    c.node('C2', 'EventTable', shape='ellipse')
    c.node('C3', 'Overview', shape='ellipse')
    c.node('C4', 'Sidebar', shape='ellipse')
    c.edges([('FR', 'C1'), ('FR', 'C2'), ('FR', 'C3'), ('FR', 'C4')])

# Add cluster for tracking service components
with dot.subgraph(name='cluster_tracking') as c:
    c.attr(label='Tracking Service Components')
    c.node('TS1', 'EventsController', shape='ellipse')
    c.node('TS2', 'Subscriber', shape='ellipse')
    c.edges([('TR', 'TS1'), ('TR', 'TS2')])

# Add cluster for user service components
with dot.subgraph(name='cluster_user') as c:
    c.attr(label='User Service Components')
    c.node('US1', 'UsersController', shape='ellipse')
    c.node('US2', 'AuthenticationController', shape='ellipse')
    c.edges([('US', 'US1'), ('US', 'US2')])

# Render the diagram to a file
dot.render('event_tracking_system_architecture', format='png', cleanup=True)
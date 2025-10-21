from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='HeyBlue Architecture')

# Define nodes for key components
dot.node('UM', 'User Management', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('IG', 'Interaction & Gamification', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('CO', 'Commerce', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('CM', 'Content Management', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('DA', 'Data Archiving & Analytics', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('NM', 'Notification & Messaging', shape='rectangle', style='filled', fillcolor='lavender')
dot.node('SP', 'Security and Privacy', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('API', 'API Gateway', shape='ellipse', style='dashed')

# Define edges for interactions
dot.edge('UM', 'API', label='Authenticate/Register', arrowhead='vee')
dot.edge('IG', 'API', label='Connect/Score', arrowhead='vee')
dot.edge('CO', 'API', label='Manage Products', arrowhead='vee')
dot.edge('CM', 'API', label='Serve Content', arrowhead='vee')
dot.edge('DA', 'API', label='Generate Reports', arrowhead='vee')
dot.edge('NM', 'API', label='Trigger Notifications', arrowhead='vee')
dot.edge('SP', 'API', label='Enforce Policies', arrowhead='vee')

# Define interactions with AWS services
dot.node('AWS', 'AWS Services', shape='rectangle', style='filled', fillcolor='lightgoldenrod')
dot.edge('API', 'AWS', label='Use Services', arrowhead='vee')

# Define the style as microservices and event-driven
dot.attr(rankdir='LR')
dot.attr('node', shape='rectangle')

# Render the graph to a file
dot.render('heyblue_architecture', format='png', cleanup=True)
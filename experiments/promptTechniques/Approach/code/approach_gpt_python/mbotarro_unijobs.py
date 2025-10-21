from graphviz import Digraph

# Create Digraph object
dot = Digraph(comment='UniJobs Architecture')

# Frontend Components
dot.node('RN_Frontend', 'React Native Frontend', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Authentication', 'User Authentication', shape='rectangle')
dot.node('Feed', 'Offer/Request Feed', shape='rectangle')
dot.node('Creation', 'Offer/Request Creation', shape='rectangle')
dot.node('Profiles', 'User Profiles', shape='rectangle')
dot.node('Navigation', 'Navigation', shape='rectangle')
dot.node('Design', 'UI Design', shape='rectangle')
dot.node('Interest', 'Interest Matching', shape='rectangle')

# Backend Components
dot.node('Go_Backend', 'Go Backend', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('REST_API', 'RESTful API', shape='rectangle')
dot.node('PostgreSQL', 'PostgreSQL Database', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('Elasticsearch', 'Elasticsearch', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('DAL', 'Data Abstraction Layer', shape='rectangle')
dot.node('BusinessLogic', 'Business Logic', shape='rectangle')

# Connect Frontend Components
dot.edge('RN_Frontend', 'Authentication')
dot.edge('RN_Frontend', 'Feed')
dot.edge('RN_Frontend', 'Creation')
dot.edge('RN_Frontend', 'Profiles')
dot.edge('RN_Frontend', 'Navigation')
dot.edge('RN_Frontend', 'Design')
dot.edge('RN_Frontend', 'Interest')

# Connect Backend Components
dot.edge('Go_Backend', 'REST_API')
dot.edge('REST_API', 'PostgreSQL', label='Manage Data')
dot.edge('REST_API', 'Elasticsearch', label='Full Text Search')
dot.edge('Go_Backend', 'DAL')
dot.edge('Go_Backend', 'BusinessLogic')

# Connect Frontend to Backend
dot.edge('Authentication', 'REST_API', label='API Call')
dot.edge('Feed', 'REST_API', label='API Call')
dot.edge('Creation', 'REST_API', label='API Call')
dot.edge('Profiles', 'REST_API', label='API Call')
dot.edge('Interest', 'REST_API', label='API Call')

# Render the diagram
dot.render('unijobs_architecture', format='png', cleanup=True)
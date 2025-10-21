from graphviz import Digraph

dot = Digraph(comment='neighbor-army_help-with-covid Architecture')

# Frontend Components
dot.node('F1', 'Next.js Frontend', shape='box', style='filled', color='lightblue')
dot.node('F1.1', 'index.js (Homepage)', shape='component')
dot.node('F1.2', 'offer-help.js (Volunteer Signup)', shape='component')
dot.node('F1.3', 'request-help.js (Request Help)', shape='component')
dot.node('F1.4', 'auth.js (Authentication)', shape='component')
dot.node('F1.5', 'AddressInput (Google Maps API)', shape='component')

# Backend Components
dot.node('B1', 'Firebase Functions Backend', shape='box', style='filled', color='lightcoral')
dot.node('B1.1', 'Task Management (Onfleet)', shape='component')
dot.node('B1.2', 'API Endpoints (Express)', shape='component')
dot.node('B1.3', 'Team Management (Firestore)', shape='component')
dot.node('B1.4', 'Worker Management (Sendgrid)', shape='component')
dot.node('B1.5', 'Phone Verification (Twilio)', shape='component')

# External Services
dot.node('S1', 'Onfleet', shape='box', style='filled', color='lightgreen')
dot.node('S2', 'Sendgrid', shape='box', style='filled', color='lightgreen')
dot.node('S3', 'Google Maps API', shape='box', style='filled', color='lightgreen')
dot.node('S4', 'Twilio', shape='box', style='filled', color='lightgreen')

# Relationships
dot.edges([
    ('F1.5', 'S3'),
    ('B1.1', 'S1'),
    ('B1.4', 'S2'),
    ('B1.5', 'S4')
])

# Connections between frontend and backend
dot.edge('F1.4', 'B1.2', label='Cookie-based Auth', dir='both')
dot.edge('F1.3', 'B1.2', label='Request Help', dir='both')
dot.edge('F1.2', 'B1.2', label='Offer Help', dir='both')

# Legend
dot.node('L1', 'Legend', shape='note', style='filled', color='lightyellow')
dot.edge('L1', 'F1', label='Frontend Components', style='dashed')
dot.edge('L1', 'B1', label='Backend Components', style='dashed')
dot.edge('L1', 'S1', label='External Services', style='dashed')

dot.render('neighbor-army_help-with-covid_architecture', format='png', cleanup=True)
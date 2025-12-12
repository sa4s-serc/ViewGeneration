from graphviz import Digraph

g = Digraph('G', filename='munchout_architecture.gv', format='png')
g.attr(rankdir='TB')

# Define styles
g.attr('node', shape='box', style='rounded,filled', fillcolor='white')
g.attr('edge', fontsize='10')

# Create Frontend cluster
with g.subgraph(name='cluster_0') as c:
    c.attr(label='Frontend (Flutter)', style='rounded', color='blue', bgcolor='lightblue')
    
    # Frontend components
    c.node('app', 'App\n(app.dart)\nMain Application Widget')
    c.node('auth', 'Authentication\n(BLoC Pattern)')
    c.node('repos', 'Repositories\n(User, Restaurant, Customer)')
    c.node('api', 'Flask API Client\n(REST Interface)')
    
    # Frontend connections
    c.edge('app', 'auth')
    c.edge('auth', 'repos')
    c.edge('repos', 'api')

# Create Backend cluster
with g.subgraph(name='cluster_1') as c:
    c.attr(label='Backend (Flask)', style='rounded', color='darkgreen', bgcolor='lightgreen')
    
    # Backend components
    c.node('flask', 'Flask App\n(app.py)')
    c.node('rest', 'REST Resources\n(Customer, Restaurant,\nEvent, Booking)')
    c.node('models', 'Data Models\n(SQLAlchemy)')
    c.node('db', 'Database', shape='cylinder')
    
    # Backend connections
    c.edge('flask', 'rest')
    c.edge('rest', 'models')
    c.edge('models', 'db')

# Connect frontend to backend
g.edge('api', 'flask', 'REST API Calls', style='bold')

# Set graph title
g.attr(label='MunchOut Application Architecture', labelloc='t', fontsize='20')

g.render(directory='.', view=False, cleanup=True)
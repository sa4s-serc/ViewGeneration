from graphviz import Digraph

dot = Digraph(comment='Restaurant Reservation System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Create main layers
dot.node('frontend', 'Frontend\n(React)', color='blue')
dot.node('backend', 'Backend\n(Node.js/Express)', color='green')
dot.node('db', 'Database\n(PostgreSQL)', color='orange')

# Create components
with dot.subgraph(name='cluster_frontend') as f:
    f.attr(label='Frontend Components')
    f.node('dashboard', 'Dashboard')
    f.node('reservations', 'Reservation Management')
    f.node('tables', 'Table Management')
    f.node('search', 'Search')

with dot.subgraph(name='cluster_backend') as b:
    b.attr(label='Backend Components')
    b.node('api', 'RESTful API')
    b.node('validation', 'Data Validation')
    b.node('controllers', 'Controllers')
    b.node('services', 'Services')

# Define relationships
dot.edge('frontend', 'backend', 'HTTP/REST')
dot.edge('backend', 'db', 'Knex.js')

# Frontend component relationships
dot.edge('dashboard', 'api')
dot.edge('reservations', 'api')
dot.edge('tables', 'api')
dot.edge('search', 'api')

# Backend component relationships
dot.edge('api', 'validation')
dot.edge('validation', 'controllers')
dot.edge('controllers', 'services')
dot.edge('services', 'db')

# Generate diagram
dot.render('restaurant_reservation_architecture', format='png', cleanup=True)
from graphviz import Digraph

dot = Digraph(comment='Event Tracking System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Frontend
dot.node('frontend', 'Frontend\n(React)')

# Gateway Service
dot.node('gateway', 'Gateway Service\n(Node.js/Express)')

# Backend Services
with dot.subgraph(name='cluster_backend') as c:
    c.attr(label='Backend Services')
    c.node('user_service', 'User Service\n(Node.js/Express)')
    c.node('tracking_service', 'Tracking Service\n(Node.js/Express)')

# Databases
dot.node('postgres_db', 'PostgreSQL', shape='cylinder')
dot.node('redis', 'Redis\n(Pub/Sub)', shape='cylinder')

# Add edges
dot.edge('frontend', 'gateway')
dot.edge('gateway', 'user_service')
dot.edge('gateway', 'tracking_service')
dot.edge('user_service', 'postgres_db')
dot.edge('tracking_service', 'postgres_db')
dot.edge('gateway', 'redis')
dot.edge('tracking_service', 'redis')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr(rankdir='TB')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('event_tracking_architecture', format='png', cleanup=True)
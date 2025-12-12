from graphviz import Digraph

dot = Digraph(comment='FAS Web App Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Create main components
dot.node('UI', 'Frontend\n(React App)')
dot.node('AUTH', 'Authentication\n(Firebase)')
dot.node('API', 'Backend API\n(Node.js)')
dot.node('DB', 'Database\n(MongoDB)')
dot.node('SENTIMENT', 'Sentiment Analysis\n(Python)')
dot.node('KAFKA', 'Kafka\nMessage Queue')

# Create connections
dot.edge('UI', 'AUTH', 'authenticate')
dot.edge('UI', 'API', 'HTTP/REST')
dot.edge('API', 'DB', 'queries/updates')
dot.edge('API', 'KAFKA', 'publish')
dot.edge('KAFKA', 'SENTIMENT', 'consume')
dot.edge('SENTIMENT', 'DB', 'store results')

# Add subgraph for frontend components
with dot.subgraph(name='cluster_frontend') as front:
    front.attr(label='Frontend Components')
    front.node('SEARCH', 'Search Component')
    front.node('DASHBOARD', 'Dashboard')
    front.node('CHARTS', 'Data Visualization')
    front.edge('SEARCH', 'DASHBOARD', 'updates')
    front.edge('DASHBOARD', 'CHARTS', 'data')

dot.edge('UI', 'SEARCH', 'contains')

print(dot.source)
dot.render('fas_architecture', view=True, format='png')
from graphviz import Digraph

dot = Digraph(comment='Partydeck Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('panel', 'Panel\n(React Frontend)\nCard Deck Management\nUser Authentication')
dot.node('server', 'Server\n(Java Backend)\nWebSocket + Game Logic')
dot.node('game', 'Game\n(React Frontend)\nGameplay Interface')
dot.node('gcloud', 'Google Cloud Run\nDeployment Platform')

# Add connections
dot.edge('panel', 'server', 'REST API')
dot.edge('game', 'server', 'WebSocket')
dot.edge('server', 'gcloud', 'Deployed on')
dot.edge('panel', 'gcloud', 'Deployed on')
dot.edge('game', 'gcloud', 'Deployed on')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('partydeck_architecture', format='png', cleanup=True)
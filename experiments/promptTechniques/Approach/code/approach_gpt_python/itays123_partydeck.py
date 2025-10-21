from graphviz import Digraph

dot = Digraph(comment='Partydeck Microservices Architecture', format='png')

# Components
dot.node('P', 'Panel (React Frontend)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('S', 'Server (Java Backend)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('G', 'Game (React Frontend)', shape='rectangle', style='filled', fillcolor='lightgreen')

# Nodes
dot.node('DB', 'Database', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('GCP', 'Google Cloud Platform', shape='rectangle', style='filled', fillcolor='lightyellow')

# Connectors
dot.edge('P', 'S', label='REST API', arrowhead='normal', style='dashed')
dot.edge('S', 'G', label='WebSocket', arrowhead='normal', style='dashed')
dot.edge('S', 'DB', label='JDBC', arrowhead='normal', style='dashed')
dot.edge('P', 'GCP', label='Deployed on', arrowhead='normal')
dot.edge('S', 'GCP', label='Deployed on', arrowhead='normal')
dot.edge('G', 'GCP', label='Deployed on', arrowhead='normal')

dot.render('partydeck_architecture_diagram')
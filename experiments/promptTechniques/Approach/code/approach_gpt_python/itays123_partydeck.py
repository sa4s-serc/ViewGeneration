from graphviz import Digraph

dot = Digraph(comment='Partydeck Microservices Architecture')

# Define nodes for microservices
dot.node('P', 'Panel (React Frontend)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('S', 'Server (Java Backend)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('G', 'Game (React Frontend)', shape='rectangle', style='filled', fillcolor='lightgreen')

# Define nodes for services and databases
dot.node('Auth', 'User Authentication Service', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('WebSocket', 'WebSocket Communication', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('GameLogic', 'Game Logic Service', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('DB', 'Database', shape='cylinder', style='filled', fillcolor='orange')

# Define edges for communication
dot.edge('P', 'Auth', label='REST API', style='dashed')
dot.edge('P', 'S', label='REST API', style='dashed')
dot.edge('S', 'WebSocket', label='WebSocket')
dot.edge('WebSocket', 'G', label='WebSocket')
dot.edge('S', 'GameLogic', label='Internal Call', style='dotted')
dot.edge('S', 'DB', label='JDBC', style='dotted')

# Add legend
dot.node('Legend', 'Legend', shape='none', width='0', height='0', style='invis')
dot.edge('Legend', 'P', label='Microservices', style='invis')
dot.edge('Legend', 'Auth', label='Services', style='invis')
dot.edge('Legend', 'DB', label='Database', style='invis')

# Render the diagram
dot.render('partydeck_architecture', format='png', cleanup=True)
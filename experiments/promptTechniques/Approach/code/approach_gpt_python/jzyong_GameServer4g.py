from graphviz import Digraph

# Initialize the diagram
dot = Digraph(comment='GameServer4g Framework', format='png')
dot.attr(rankdir='LR', size='10,10')

# Define nodes with color coding for different services
dot.node('Gate', 'Gate (Gateway)', shape='rect', style='filled', color='lightblue')
dot.node('Hall', 'Hall Server', shape='rect', style='filled', color='lightgreen')
dot.node('World', 'World Server', shape='rect', style='filled', color='lightcoral')
dot.node('Resource', 'Resource Server', shape='rect', style='filled', color='lightgoldenrod')
dot.node('API', 'API (Login/Charge)', shape='rect', style='filled', color='lightgrey')
dot.node('Manager', 'Manager (HTTP Services)', shape='rect', style='filled', color='lightpink')
dot.node('Zookeeper', 'ZooKeeper', shape='rect', style='filled', color='lightyellow')

# Define clients and network components
dot.node('Client', 'Client', shape='rect', style='filled', color='white')
dot.node('gRPC', 'gRPC', shape='rect', style='filled', color='white')

# Define edges with communication protocols
dot.edge('Client', 'Gate', label='TCP', style='dashed')
dot.edge('Gate', 'Hall', label='gRPC', style='dashed')
dot.edge('Hall', 'World', label='gRPC', style='dashed')
dot.edge('World', 'Resource', label='gRPC', style='dashed')
dot.edge('Gate', 'Manager', label='HTTP', style='dashed')
dot.edge('Gate', 'API', label='HTTP', style='dashed')

# Service Discovery and Configuration
dot.edge('Gate', 'Zookeeper', label='Service Discovery', style='dotted')
dot.edge('Hall', 'Zookeeper', label='Service Discovery', style='dotted')
dot.edge('World', 'Zookeeper', label='Service Discovery', style='dotted')

# Render the diagram
dot.render('gameserver4g_framework_diagram')
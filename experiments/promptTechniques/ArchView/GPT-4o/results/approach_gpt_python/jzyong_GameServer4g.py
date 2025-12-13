from graphviz import Digraph

dot = Digraph(comment='GameServer4g Architecture', format='png')

# Creating nodes for each component
dot.node('Gate', 'Gate (Gateway)')
dot.node('Hall', 'Hall Server')
dot.node('World', 'World Server')
dot.node('Resource', 'Resource Server')
dot.node('API', 'API (Login/Charge)')
dot.node('Manager', 'Manager (Admin Services)')
dot.node('GameService', 'Game-service')
dot.node('ZooKeeper', 'ZooKeeper')

# Creating edges to represent communication
dot.edge('Gate', 'Hall', label='gRPC')
dot.edge('Hall', 'World', label='gRPC')
dot.edge('World', 'Hall', label='gRPC')
dot.edge('Gate', 'ZooKeeper', label='Service Discovery')
dot.edge('Hall', 'ZooKeeper', label='Service Discovery')
dot.edge('World', 'ZooKeeper', label='Service Discovery')
dot.edge('Gate', 'API', label='Custom TCP')
dot.edge('Gate', 'Manager', label='HTTP')

# Render the diagram
dot.render('gameserver4g_architecture')
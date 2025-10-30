from graphviz import Digraph

dot = Digraph(comment='Foundry System Architecture')

# Define nodes
dot.node('F', 'Furnace')
dot.node('PM', 'Package Management')
dot.node('MH', 'Metrics and Health Checks')
dot.node('OS', 'Object Storage Integration')
dot.node('BI', 'Builder Interface')
dot.node('GRPC', 'gRPC Interface')

# Define edges
dot.edge('F', 'PM', 'Tracks package state')
dot.edge('F', 'MH', 'Provides metrics and health checks')
dot.edge('F', 'OS', 'Uploads packages')
dot.edge('F', 'BI', 'Utilizes builder interface')
dot.edge('F', 'GRPC', 'Exposes gRPC for build requests')

# Render the diagram
dot.render('foundry_architecture', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='HikariKeeper Architecture', format='png')

# Define nodes with specific styles for different components
dot.node('Raft', 'Raft Consensus', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Meta', 'Metadata Storage', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Disc', 'Discovery Service', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('Client', 'Client API', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('Spring', 'Spring Boot Integration', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('Bench', 'Benchmarking', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('Coord', 'Coordination Service', shape='rectangle', style='filled', fillcolor='lightcyan')

# Define edges to represent communication paths
dot.edge('Client', 'Raft', label='RPC Calls', arrowhead='vee')
dot.edge('Raft', 'Meta', label='Log Replication', arrowhead='vee')
dot.edge('Raft', 'Disc', label='Service Discovery', arrowhead='vee')
dot.edge('Disc', 'Client', label='Service Lookup', arrowhead='vee')
dot.edge('Client', 'Spring', label='Integration', arrowhead='vee')
dot.edge('Bench', 'Raft', label='Performance Metrics', arrowhead='vee')
dot.edge('Coord', 'Raft', label='Synchronization', arrowhead='vee')

# Render the graph to a file
dot.render('hikarikeeper_architecture', view=True)
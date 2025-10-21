from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Meshery Architecture')

# Add nodes for key components
dot.node('A', 'Meshery Server', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'Meshery UI', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('C', 'mesheryctl (CLI)', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('D', 'Meshery Operator', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('E', 'Adapters', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('F', 'MeshSync', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('G', 'GraphQL API', shape='rectangle', style='filled', fillcolor='lightcyan')
dot.node('H', 'Event Broker', shape='rectangle', style='filled', fillcolor='lightgoldenrod')

# Add edges to represent communication
dot.edge('A', 'B', label='gRPC')
dot.edge('A', 'C', label='gRPC')
dot.edge('A', 'D', label='gRPC')
dot.edge('A', 'E', label='gRPC')
dot.edge('A', 'F', label='gRPC')
dot.edge('A', 'G', label='gRPC')
dot.edge('A', 'H', label='NATS')

# Add additional edges for communication
dot.edge('B', 'G', label='GraphQL')
dot.edge('C', 'A', label='Command Pattern')
dot.edge('D', 'F', label='MeshSync Management')
dot.edge('E', 'A', label='Adapter Pattern')
dot.edge('F', 'A', label='State Sync')
dot.edge('H', 'F', label='Event Notification')

# Render the graph to a file
dot.render('meshery_architecture_diagram', format='png', cleanup=True)

# View the graph
dot.view()
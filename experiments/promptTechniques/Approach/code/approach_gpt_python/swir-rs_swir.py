from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='SWIR Architecture')

# Define nodes for each component/subsystem
dot.node('A', 'SWIR Sidecar Service', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'HTTP/HTTPS Server', shape='rectangle')
dot.node('C', 'gRPC Server', shape='rectangle')
dot.node('D', 'Message Brokers', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('E', 'Persistence Stores', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('F', 'Service Discovery', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('G', 'Metrics and Tracing', shape='rectangle')
dot.node('H', 'Configuration Management', shape='rectangle')

# Define sub-nodes for message brokers
dot.node('D1', 'Kafka', shape='ellipse')
dot.node('D2', 'NATS', shape='ellipse')
dot.node('D3', 'AWS Kinesis', shape='ellipse')

# Define sub-nodes for persistence stores
dot.node('E1', 'Redis', shape='ellipse')
dot.node('E2', 'DynamoDB', shape='ellipse')

# Define sub-nodes for service discovery
dot.node('F1', 'mDNS', shape='ellipse')
dot.node('F2', 'DynamoDB', shape='ellipse')

# Define edges to represent communication and dependencies
dot.edge('A', 'B', label='Handles HTTP Requests')
dot.edge('A', 'C', label='Handles gRPC Requests')
dot.edge('B', 'D', label='PubSub via HTTP')
dot.edge('C', 'D', label='PubSub via gRPC')
dot.edge('B', 'E', label='Data Persistence HTTP')
dot.edge('C', 'E', label='Data Persistence gRPC')
dot.edge('B', 'F', label='Service Invocation HTTP')
dot.edge('C', 'F', label='Service Invocation gRPC')
dot.edge('A', 'G', label='Collects Metrics & Tracing')
dot.edge('A', 'H', label='Loads Configurations')

# Internal communications for message brokers
dot.edge('D', 'D1', style='dashed')
dot.edge('D', 'D2', style='dashed')
dot.edge('D', 'D3', style='dashed')

# Internal communications for persistence stores
dot.edge('E', 'E1', style='dashed')
dot.edge('E', 'E2', style='dashed')

# Internal communications for service discovery
dot.edge('F', 'F1', style='dashed')
dot.edge('F', 'F2', style='dashed')

# Render and view the diagram
dot.render('swir_architecture_diagram', format='png', cleanup=True)
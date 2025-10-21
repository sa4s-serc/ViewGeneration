from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Libre Core/Platform Architecture')

# Define nodes for the architectural components
dot.node('A', 'Libre Core', shape='rectangle')
dot.node('B', 'Docker Compose Setup', shape='rectangle')
dot.node('C', 'Libre Administration UI', shape='rectangle')
dot.node('D', 'GraphQL API', shape='rectangle')
dot.node('E', 'Grafana Dashboards', shape='rectangle')
dot.node('F', 'MQTT Broker (EMQX)', shape='rectangle')
dot.node('G', 'Workflow Engine', shape='rectangle')
dot.node('H', 'Data Provider Interface', shape='rectangle')

# Define nodes for databases
dot.node('I', 'Dgraph', shape='cylinder')
dot.node('J', 'InfluxDB', shape='cylinder')

# Define edges to represent communication and interactions
dot.edge('B', 'A', label='Deploys')
dot.edge('B', 'C', label='Deploys')
dot.edge('B', 'D', label='Deploys')
dot.edge('B', 'E', label='Deploys')
dot.edge('B', 'F', label='Deploys')
dot.edge('B', 'G', label='Deploys')
dot.edge('B', 'H', label='Deploys')

dot.edge('D', 'I', label='Queries', style='dashed')
dot.edge('E', 'J', label='Visualizes', style='dashed')
dot.edge('F', 'G', label='Event-Driven', style='dashed')
dot.edge('H', 'F', label='Uses', style='dashed')

# Add a legend
with dot.subgraph(name='cluster_legend') as c:
    c.attr(label='Legend')
    c.node('L1', 'Component', shape='rectangle')
    c.node('L2', 'Database', shape='cylinder')
    c.edge('L3', 'L1', label='Deployment')
    c.edge('L4', 'L2', label='Interaction', style='dashed')

# Render the graph to a file
dot.render('libre_core_platform_architecture', format='png', cleanup=True)

# Output diagram source code
print(dot.source)
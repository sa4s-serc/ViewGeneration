import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Libre Core/Platform Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='filled,rounded', fillcolor='lightblue')
dot.attr('edge', color='darkblue')

# Create subgraph for storage layer
with dot.subgraph(name='cluster_0') as storage:
    storage.attr(label='Data Storage Layer', style='filled', fillcolor='lightgrey')
    storage.attr('node', shape='cylinder', style='filled', fillcolor='lightgreen')
    storage.node('influxdb', 'InfluxDB\n(Time Series)')
    storage.node('dgraph', 'Dgraph\n(Primary DB)')

# Create subgraph for middleware layer
with dot.subgraph(name='cluster_1') as middleware:
    middleware.attr(label='Middleware Layer', style='filled', fillcolor='lightgrey')
    middleware.attr('node', shape='rectangle', style='filled,rounded')
    middleware.node('graphql', 'GraphQL API\n(Federation/Gateway)', fillcolor='yellow')
    middleware.node('mqtt', 'MQTT Broker\n(EMQX)', fillcolor='orange')
    middleware.node('workflow', 'Workflow Engine', fillcolor='orange')

# Create subgraph for application layer
with dot.subgraph(name='cluster_2') as apps:
    apps.attr(label='Application Layer', style='filled', fillcolor='lightgrey')
    apps.attr('node', shape='rectangle', style='filled,rounded', fillcolor='lightblue')
    apps.node('admin_ui', 'Libre Admin UI\n(Central Management)')
    apps.node('grafana', 'Grafana\n(Visualization)')
    apps.node('core', 'Libre Core\n(System Demo)')
    apps.node('packml', 'PackML Simulator')
    apps.node('dataprovider', 'Data Provider\nInterface')

# Add connections
dot.edge('admin_ui', 'graphql', 'REST/GraphQL')
dot.edge('core', 'graphql', 'GraphQL')
dot.edge('graphql', 'dgraph', 'Queries/Mutations')
dot.edge('packml', 'mqtt', 'Events')
dot.edge('mqtt', 'workflow', 'Events')
dot.edge('workflow', 'graphql', 'Updates')
dot.edge('dataprovider', 'mqtt', 'Data')
dot.edge('dataprovider', 'influxdb', 'Metrics')
dot.edge('grafana', 'influxdb', 'Queries')

# Save the diagram
dot.render('libre_architecture', format='png', cleanup=True)
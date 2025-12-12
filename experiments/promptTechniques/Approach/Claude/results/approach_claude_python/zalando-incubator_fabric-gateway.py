import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Fabric Gateway Architecture')
dot.attr(rankdir='TB')

# Set global node and edge styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Create clusters/subgraphs for logical grouping
with dot.subgraph(name='cluster_0') as control_plane:
    control_plane.attr(label='Control Plane', style='rounded', color='blue')
    control_plane.node('crd', 'FabricGateway CRD\nCore Configuration')
    control_plane.node('operator', 'Gateway Operator')
    control_plane.node('webhook', 'Validation Webhooks')
    control_plane.node('stackset', 'StackSets')

with dot.subgraph(name='cluster_1') as data_plane:
    data_plane.attr(label='Data Plane', style='rounded', color='green')
    data_plane.node('ingress', 'Ingress Resources')
    data_plane.node('skipper', 'Skipper Routes')
    data_plane.node('iam', 'Zalando IAM')

with dot.subgraph(name='cluster_2') as policy:
    policy.attr(label='Policy Enforcement', style='rounded', color='red')
    policy.node('auth', 'Authentication')
    policy.node('authz', 'Authorization')
    policy.node('rate', 'Rate Limiting')
    policy.node('cors', 'CORS')

# Add testing components
dot.node('e2e', 'E2E Tests', shape='hexagon')
dot.node('docs', 'Documentation\n(MkDocs)', shape='note')

# Add edges to show relationships
dot.edge('crd', 'operator', 'configures')
dot.edge('operator', 'ingress', 'generates')
dot.edge('operator', 'skipper', 'configures')
dot.edge('stackset', 'operator', 'service discovery')
dot.edge('webhook', 'crd', 'validates')
dot.edge('ingress', 'skipper', 'routes traffic')
dot.edge('skipper', 'iam', 'authenticates')

# Policy enforcement flows
dot.edge('skipper', 'auth', 'enforces')
dot.edge('auth', 'authz')
dot.edge('authz', 'rate')
dot.edge('rate', 'cors')

# Testing relationships
dot.edge('e2e', 'crd', 'validates')
dot.edge('e2e', 'skipper', 'tests')

# Save the diagram
dot.render('fabric_gateway_architecture', format='png', cleanup=True)
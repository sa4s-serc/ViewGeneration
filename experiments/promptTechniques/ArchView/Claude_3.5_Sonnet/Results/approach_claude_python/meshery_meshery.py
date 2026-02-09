from graphviz import Digraph

dot = Digraph(comment='Meshery Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')

# Add main components
dot.node('server', 'Meshery Server\n(Core)')
dot.node('ui', 'Meshery UI\n(React/Next.js)')
dot.node('operator', 'Meshery Operator')
dot.node('meshsync', 'MeshSync')
dot.node('broker', 'Event Broker\n(NATS)')
dot.node('adapters', 'Service Mesh\nAdapters')
dot.node('providers', 'Providers\n(Local/Remote)')
dot.node('graphql', 'GraphQL API')
dot.node('k8s', 'Kubernetes\nClusters')

# Add connections
dot.edge('ui', 'server', 'gRPC/REST')
dot.edge('server', 'graphql', 'Queries/Mutations')
dot.edge('server', 'adapters', 'gRPC')
dot.edge('server', 'providers', 'Auth/Storage')
dot.edge('operator', 'meshsync', 'Manages')
dot.edge('meshsync', 'k8s', 'Monitors')
dot.edge('meshsync', 'broker', 'Events')
dot.edge('broker', 'server', 'Events')
dot.edge('adapters', 'k8s', 'Configure\nMeshes')
dot.edge('server', 'k8s', 'Control')

# Add subgraph for adapters
with dot.subgraph(name='cluster_adapters') as c:
    c.attr(label='Service Mesh Adapters')
    c.node('istio', 'Istio')
    c.node('linkerd', 'Linkerd')
    c.node('consul', 'Consul')
    c.edge('adapters', 'istio')
    c.edge('adapters', 'linkerd')
    c.edge('adapters', 'consul')

dot.render('meshery_architecture', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Foundry Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Create clusters for logical grouping
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Build System', style='rounded', color='gray')
    c.node('furnace', 'Furnace\nCore Build Component')
    c.node('builder', 'MakepkgBuilder\nPackage Building')
    c.node('queue', 'Build Queue\nAsync Processing')
    c.node('pkgmap', 'Package Map\nState Management')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='External Systems', style='rounded', color='gray')
    c.node('aur', 'AUR\nPackage Source')
    c.node('storage', 'Object Storage\nBuilt Packages')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Monitoring & Interface', style='rounded', color='gray')
    c.node('metrics', 'Prometheus\nMetrics & Monitoring')
    c.node('grpc', 'gRPC Interface\nClient Communication')

# Add edges with descriptions
dot.edge('aur', 'furnace', 'Package Info')
dot.edge('furnace', 'builder', 'Build Request')
dot.edge('builder', 'storage', 'Upload Package')
dot.edge('furnace', 'metrics', 'Performance Data')
dot.edge('furnace', 'queue', 'Queue Build')
dot.edge('queue', 'builder', 'Process Build')
dot.edge('furnace', 'pkgmap', 'Track State')
dot.edge('grpc', 'furnace', 'Client Requests')

# Save the diagram
dot.render('foundry_architecture', format='png', cleanup=True)
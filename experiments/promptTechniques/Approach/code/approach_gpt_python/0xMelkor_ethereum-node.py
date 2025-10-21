from graphviz import Digraph

dot = Digraph(comment='Ethereum Node Deployment on GKE')

# Define nodes
dot.node('Geth', 'Geth (Execution Layer)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Lighthouse', 'Lighthouse (Consensus Layer)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('InfluxDB', 'InfluxDB', shape='rectangle', style='filled', fillcolor='orange')
dot.node('Nginx', 'Nginx (Reverse Proxy)', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('K8s', 'Kubernetes', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('GCB', 'Google Cloud Build', shape='rectangle', style='filled', fillcolor='yellow')

# Define edges
dot.edge('Geth', 'InfluxDB', 'Metrics Collection', arrowhead='normal')
dot.edge('Geth', 'Nginx', 'RPC/WS Exposure', arrowhead='normal')
dot.edge('Lighthouse', 'InfluxDB', 'Metrics Collection', arrowhead='normal')
dot.edge('Nginx', 'External', 'Exposes Endpoints', arrowhead='normal', dir='both')
dot.edge('GCB', 'K8s', 'Automated Deployment', arrowhead='normal')

# Define clusters
with dot.subgraph(name='cluster_0') as c:
    c.attr(style='filled', color='lightgrey')
    c.node_attr.update(style='filled', color='white')
    c.edges([('Geth', 'Lighthouse')])
    c.attr(label='Ethereum Node')

with dot.subgraph(name='cluster_1') as c:
    c.attr(style='filled', color='lightgrey')
    c.node_attr.update(style='filled', color='white')
    c.node('InternalNetwork', 'K8s Service Discovery', shape='ellipse', style='filled', fillcolor='lightyellow')
    c.edge('InternalNetwork', 'Geth')
    c.edge('InternalNetwork', 'Lighthouse')
    c.edge('InternalNetwork', 'InfluxDB')

# Render the diagram
dot.render('ethereum_node_deployment_gke', format='png', cleanup=True)
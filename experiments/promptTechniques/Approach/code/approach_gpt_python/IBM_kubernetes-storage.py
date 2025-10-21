from graphviz import Digraph

# Initialize the Digraph
dot = Digraph(comment='Kubernetes Storage Workshop Architecture')

# Define node styles
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')

# Components
dot.node('A', 'Guestbook Application (Node.js)')
dot.node('B', 'IBM Cloud Object Storage')
dot.node('C', 'IBM Cloud Block Storage')
dot.node('D', 'Kubernetes Cluster')
dot.node('E', 'Helm Chart for MongoDB')
dot.node('F', 'ConfigMaps and Secrets')
dot.node('G', 'IBM Cloud Operator')

# Grouping within Kubernetes Cluster
with dot.subgraph(name='cluster_k8s') as c:
    c.attr(style='dashed', color='blue')
    c.node_attr.update(style='filled', color='lightyellow')
    c.node('D1', 'StatefulSets')
    c.node('D2', 'Persistent Volumes & Claims')
    c.edge('D1', 'D2', label='Manages')

# Connectors and Interactions
dot.edge('A', 'D', label='Deploys to', dir='forward')
dot.edge('A', 'B', label='Accesses', dir='forward')
dot.edge('A', 'C', label='Accesses', dir='forward')
dot.edge('D', 'E', label='Uses', dir='forward')
dot.edge('D', 'F', label='Uses', dir='forward')
dot.edge('D', 'G', label='Manages', dir='forward')
dot.edge('G', 'B', label='Provision', dir='bidirectional')
dot.edge('G', 'C', label='Provision', dir='bidirectional')

# Render the diagram
dot.render('kubernetes_storage_workshop_architecture', format='png', cleanup=True)
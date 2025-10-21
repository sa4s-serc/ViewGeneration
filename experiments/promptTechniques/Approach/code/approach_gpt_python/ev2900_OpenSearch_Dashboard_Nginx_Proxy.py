from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='OpenSearch Dashboard Nginx Proxy Architecture')

# Define nodes
dot.node('A', 'Internet', shape='cloud')
dot.node('B', 'Nginx Proxy (Public Subnet)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('C', 'OpenSearch Dashboard (Private Subnet)', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('D', 'Security Groups', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('E', 'VPC', shape='rectangle', style='filled', fillcolor='lightcoral')

# Define edges
dot.edge('A', 'B', label='HTTPS')
dot.edge('B', 'C', label='Forward to OpenSearch')
dot.edge('B', 'D', label='Traffic Control')
dot.edge('C', 'D', label='Traffic Control')
dot.edge('B', 'E', style='dashed')
dot.edge('C', 'E', style='dashed')
dot.edge('D', 'E', style='dashed')

# Render the diagram
dot.render('opensearch_nginx_proxy_architecture', format='png', cleanup=True)
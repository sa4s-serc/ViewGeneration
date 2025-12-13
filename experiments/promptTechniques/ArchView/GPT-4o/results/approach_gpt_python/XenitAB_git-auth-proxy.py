from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Git Auth Proxy Architecture')

# Define nodes and their styles
dot.node('ProxyServer', 'Proxy Server', shape='rectangle', style='filled', color='lightblue')
dot.node('TokenAuth', 'Token-Based Authentication', shape='rectangle', style='filled', color='lightgreen')
dot.node('AuthLayer', 'Authorization Layer', shape='rectangle', style='filled', color='lightgreen')
dot.node('ConfigLoad', 'Configuration Loading', shape='rectangle', style='filled', color='lightyellow')
dot.node('K8sSecretMgmt', 'Kubernetes Secret Management', shape='rectangle', style='filled', color='lightyellow')
dot.node('MetricsEndpoint', 'Metrics Endpoint', shape='rectangle', style='filled', color='lightcoral')

# Define Git providers
dot.node('GitHub', 'GitHub', shape='ellipse', style='filled', color='lightgrey')
dot.node('AzureDevOps', 'Azure DevOps', shape='ellipse', style='filled', color='lightgrey')

# Define Kubernetes
dot.node('Kubernetes', 'Kubernetes', shape='ellipse', style='filled', color='lightgrey')

# Define edges and their styles
dot.edge('ProxyServer', 'GitHub', label='Forward Requests', style='dashed')
dot.edge('ProxyServer', 'AzureDevOps', label='Forward Requests', style='dashed')
dot.edge('ProxyServer', 'TokenAuth', label='Validate Token', style='bold')
dot.edge('TokenAuth', 'AuthLayer', label='Check Permissions', style='bold')
dot.edge('AuthLayer', 'ProxyServer', label='Authorize', style='bold')
dot.edge('ConfigLoad', 'ProxyServer', label='Load Config', style='dotted')
dot.edge('K8sSecretMgmt', 'Kubernetes', label='Manage Secrets', style='dotted')
dot.edge('MetricsEndpoint', 'ProxyServer', label='Expose Metrics', style='dotted')

# Define legend
dot.node('Legend', 'Legend', shape='rectangle', style='filled', color='white')
dot.node('Component', 'Component', shape='rectangle', style='filled', color='lightblue')
dot.node('Functionality', 'Functionality', shape='rectangle', style='filled', color='lightgreen')
dot.node('Process', 'Process', shape='rectangle', style='filled', color='lightyellow')
dot.node('External', 'External Service', shape='ellipse', style='filled', color='lightgrey')
dot.node('Metrics', 'Metrics', shape='rectangle', style='filled', color='lightcoral')

dot.edge('Legend', 'Component', label='Main Components', style='solid')
dot.edge('Legend', 'Functionality', label='Functionalities', style='solid')
dot.edge('Legend', 'Process', label='Processes', style='solid')
dot.edge('Legend', 'External', label='External Systems', style='solid')
dot.edge('Legend', 'Metrics', label='Metrics', style='solid')

# Render the graph
dot.render('git_auth_proxy_architecture', format='png', cleanup=True)
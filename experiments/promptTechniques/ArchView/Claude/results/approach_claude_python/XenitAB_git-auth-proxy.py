from graphviz import Digraph

dot = Digraph(comment='Git Auth Proxy Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('proxy', 'Proxy Server\n(Authentication & Authorization)')
dot.node('k8s', 'Kubernetes\nSecret Management')
dot.node('gh', 'GitHub')
dot.node('ado', 'Azure DevOps')
dot.node('metrics', 'Metrics Endpoint\n(Prometheus)')
dot.node('config', 'Configuration\nLoader')
dot.node('token', 'Token\nManagement')

# Add connections
dot.edge('gh', 'proxy', 'Git Requests')
dot.edge('ado', 'proxy', 'Git Requests')
dot.edge('proxy', 'k8s', 'Token Validation')
dot.edge('k8s', 'token', 'Secret Changes')
dot.edge('config', 'proxy', 'Load Config')
dot.edge('proxy', 'metrics', 'Expose Metrics')
dot.edge('token', 'k8s', 'Manage Secrets')

# Generate diagram
dot.render('git_auth_proxy_architecture', format='png', cleanup=True)
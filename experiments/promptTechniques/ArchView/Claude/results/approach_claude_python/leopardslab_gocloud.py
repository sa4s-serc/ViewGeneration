import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='GoCloud Architecture View')
dot.attr(rankdir='TB')

# Add styling
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
dot.attr('edge', color='darkblue')

# Add main components
dot.node('interface', 'Cloud Provider Interface\n(gocloudinterface)')
dot.node('core', 'Core Services\n(gocloud)')
dot.node('auth', 'Authentication\n(auth)')

# Add cloud providers
providers = ['AWS', 'GCP', 'Azure', 'DigitalOcean', 'Alibaba', 'Vultr', 'Rackspace', 'OpenStack']
with dot.subgraph(name='cluster_providers') as c:
    c.attr(label='Cloud Providers')
    for provider in providers:
        c.node(provider, provider)
        dot.edge('interface', provider)

# Add service categories
services = ['Compute', 'Storage', 'Container', 'DNS', 'LoadBalancer', 'Serverless', 'Database']
with dot.subgraph(name='cluster_services') as c:
    c.attr(label='Services')
    for service in services:
        c.node(service, service)
        dot.edge('core', service)

# Connect components
dot.edge('core', 'interface')
dot.edge('auth', 'interface')

# Print the DOT source
print(dot.source)

# Render the graph
dot.render('gocloud_architecture', format='png', cleanup=True)
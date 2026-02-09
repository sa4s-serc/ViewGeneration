import graphviz

# Create a new directed graph
g = graphviz.Digraph('2WAY_Design_Architecture')
g.attr(rankdir='TB')

# Add nodes
g.node('trust_network', 'Trust Network\nSystem', shape='cloud')
g.node('auth', 'Authorization &\nAuthentication', shape='component')
g.node('data_exchange', 'Secure Data\nExchange Layer', shape='box')
g.node('private_data', 'Private Data\nStorage', shape='cylinder')
g.node('identifi', 'Identifi Base\nPlatform', shape='component')

# Create subgraph for security components
with g.subgraph(name='cluster_security') as s:
    s.attr(label='Security Layer', style='rounded', color='blue')
    s.node('auth')
    s.node('trust_network')

# Create subgraph for data components
with g.subgraph(name='cluster_data') as d:
    d.attr(label='Data Layer', style='rounded', color='green')
    d.node('data_exchange')
    d.node('private_data')

# Add edges with labels
g.edge('trust_network', 'auth', 'Verification')
g.edge('auth', 'data_exchange', 'Access Control')
g.edge('data_exchange', 'private_data', 'Store/Retrieve')
g.edge('identifi', 'data_exchange', 'Foundation Services')
g.edge('identifi', 'auth', 'Identity Services')

# Set global graph attributes
g.attr(fontname='Helvetica')
g.attr('node', fontname='Helvetica')
g.attr('edge', fontname='Helvetica', color='gray')

# Save the diagram
g.render('2way_design_architecture', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='AadApiGatekeeper Architecture')

# Add nodes for key components
dot.node('RP', 'Reverse Proxy', shape='rectangle', style='filled', color='lightblue')
dot.node('AAA', 'Authentication & Authorization', shape='rectangle', style='filled', color='lightgreen')
dot.node('TA', 'Token Acquisition', shape='rectangle', style='filled', color='lightyellow')
dot.node('CFG', 'Configuration', shape='rectangle', style='filled', color='lightpink')
dot.node('PI', 'Platform Integration', shape='rectangle', style='filled', color='lightgrey')
dot.node('TC', 'Token Caching', shape='rectangle', style='filled', color='lightcyan')
dot.node('PAR', 'Public Access Routes', shape='rectangle', style='filled', color='lightcoral')
dot.node('UCR', 'User Claims Retrieval', shape='rectangle', style='filled', color='lightgoldenrod')
dot.node('LE', 'Login Endpoint', shape='rectangle', style='filled', color='lightsteelblue')

# Add edges to represent communication between components
dot.edge('RP', 'AAA', label='Validate AAD Tokens')
dot.edge('AAA', 'RP', label='Forward Requests')
dot.edge('AAA', 'TA', label='Acquire Tokens')
dot.edge('CFG', 'RP', label='Environment Variables')
dot.edge('PI', 'RP', label='Deployment Templates')
dot.edge('RP', 'TC', label='Token Caching')
dot.edge('RP', 'PAR', label='Anonymous Path Bypass')
dot.edge('AAA', 'UCR', label='Expose Claims')
dot.edge('AAA', 'LE', label='Initiate OIDC Flow')

# Add legend
with dot.subgraph(name='cluster_legend') as c:
    c.attr(label='Legend', color='black')
    c.node('Legend1', 'Component', shape='rectangle', style='filled', color='white')
    c.node('Legend2', 'Communication', shape='plaintext')
    c.edge('Legend1', 'Legend2', label='Interaction')

# Render the graph to a file
dot.render('aad_api_gatekeeper_architecture', format='png', cleanup=True)
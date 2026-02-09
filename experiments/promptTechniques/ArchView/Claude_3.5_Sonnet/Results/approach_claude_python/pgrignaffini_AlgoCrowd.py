from graphviz import Digraph

# Create a new directed graph
dot = Digraph('decentralized_crowdfunding_architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgrey')

# Create clusters
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Frontend (Next.js)', style='filled', color='lightblue')
    c.node('pages', 'Pages\n(Routes)')
    c.node('components', 'UI Components')
    c.node('api_js', 'API.js')
    c.node('app_context', 'AppContext.js')
    c.node('utils', 'Utils')
    
    # Frontend internal connections
    c.edge('pages', 'components')
    c.edge('components', 'api_js')
    c.edge('components', 'app_context')
    c.edge('app_context', 'api_js')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Backend (Express.js)', style='filled', color='lightgreen')
    c.node('server', 'server.js\n(REST API)')
    c.node('dao', 'dao.js')
    c.node('db', 'SQLite DB')
    
    # Backend internal connections
    c.edge('server', 'dao')
    c.edge('dao', 'db')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Smart Contracts (Algorand)', style='filled', color='lightyellow')
    c.node('contracts', 'contracts.py\n(PyTeal)')
    c.node('operations', 'operations.py')
    c.node('blockchain', 'Algorand\nBlockchain')
    
    # Smart contract internal connections
    c.edge('operations', 'contracts')
    c.edge('contracts', 'blockchain')

# Cross-component connections
dot.edge('api_js', 'server', 'REST API')
dot.edge('server', 'operations', 'Contract Calls')
dot.edge('app_context', 'blockchain', 'AlgoSigner')

# Set graph title
dot.attr(label='Decentralized Crowdfunding Platform Architecture\nSystem Component View', labelloc='t', fontsize='16')

# Render the graph
dot.render('crowdfunding_architecture', format='png', cleanup=True)
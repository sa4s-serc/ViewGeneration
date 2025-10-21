from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Decentralized Crowdfunding Platform Architecture')

# Add nodes for each major component
dot.node('Client', 'Next.js Application', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Server', 'Express.js Backend', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('DB', 'SQLite Database', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('SmartContracts', 'PyTeal-based Smart Contracts', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Algorand', 'Algorand Blockchain', shape='rectangle', style='filled', fillcolor='gold')

# Add edges to represent communication between components
dot.edge('Client', 'Server', label='REST API Calls', style='dashed')
dot.edge('Server', 'DB', label='SQL Queries')
dot.edge('Server', 'SmartContracts', label='Contract Interaction', style='dotted')
dot.edge('SmartContracts', 'Algorand', label='Blockchain Transactions', style='dotted')

# Add subcomponents for Client
with dot.subgraph(name='cluster_client') as c:
    c.attr(label='Client Components')
    c.node('Pages', 'Next.js Pages', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('Components', 'React Components', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('APIs', 'API.js', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('Context', 'AppContext.js', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('Constants', 'Constants', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('Utils', 'Utils', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.edge('Pages', 'Components')
    c.edge('Components', 'APIs')
    c.edge('Components', 'Context')
    c.edge('Components', 'Constants')
    c.edge('Components', 'Utils')

# Add subcomponents for Server
with dot.subgraph(name='cluster_server') as s:
    s.attr(label='Server Components')
    s.node('ServerJS', 'server.js', shape='rectangle', style='filled', fillcolor='salmon')
    s.node('DBJS', 'db.js', shape='rectangle', style='filled', fillcolor='salmon')
    s.node('DAOJS', 'dao.js', shape='rectangle', style='filled', fillcolor='salmon')
    s.edge('ServerJS', 'DBJS')
    s.edge('ServerJS', 'DAOJS')

# Add subcomponents for Smart Contracts
with dot.subgraph(name='cluster_smartcontracts') as sc:
    sc.attr(label='Smart Contract Components')
    sc.node('Contracts', 'contracts.py', shape='rectangle', style='filled', fillcolor='palegreen')
    sc.node('Operations', 'operations.py', shape='rectangle', style='filled', fillcolor='palegreen')
    sc.node('Util', 'util.py', shape='rectangle', style='filled', fillcolor='palegreen')
    sc.edge('Contracts', 'Operations')
    sc.edge('Operations', 'Util')

# Render the diagram
dot.render('crowdfunding_platform_architecture', format='png', cleanup=True)
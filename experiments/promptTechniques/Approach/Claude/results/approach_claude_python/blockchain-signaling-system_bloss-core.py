import graphviz

# Create digraph
dot = graphviz.Digraph('BloSS_Architecture', comment='BloSS Core Architecture Diagram')
dot.attr(rankdir='TB')

# Add clusters for main components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Network Layer', style='rounded', color='blue')
    c.node('stalk', 'Stalk\nNetwork Monitoring\nAttack Detection', shape='box', style='filled', fillcolor='lightblue')
    c.node('router', 'Simple Router\nPacket Forwarding', shape='box', style='filled', fillcolor='lightblue')
    c.node('stats', 'Flow Statistics\nManager', shape='box', style='filled', fillcolor='lightblue')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Core Layer', style='rounded', color='green')
    c.node('bloss', 'BloSS\nMitigation Handling\nAttack Signaling', shape='box', style='filled', fillcolor='lightgreen')
    c.node('api', 'REST API\nEndpoints', shape='box', style='filled', fillcolor='lightgreen')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Storage Layer', style='rounded', color='orange')
    c.node('pollen', 'Pollen\nBlockchain Integration', shape='box', style='filled', fillcolor='lightyellow')
    c.node('ipfs', 'IPFS Storage\nAttack Reports', shape='cylinder', style='filled', fillcolor='lightyellow')
    c.node('influx', 'InfluxDB\nTraffic Stats', shape='cylinder', style='filled', fillcolor='lightyellow')
    c.node('eth', 'Ethereum\nBlockchain', shape='cylinder', style='filled', fillcolor='lightyellow')

# Add edges
dot.edge('stalk', 'router', 'monitors')
dot.edge('router', 'stats', 'forwards stats')
dot.edge('stats', 'bloss', 'reports attacks')
dot.edge('bloss', 'api', 'exposes')
dot.edge('api', 'pollen', 'stores data')
dot.edge('pollen', 'ipfs', 'stores reports')
dot.edge('pollen', 'influx', 'stores stats')
dot.edge('pollen', 'eth', 'smart contracts')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr(label='BloSS Core Architecture\nBlockchain-based DDoS Defense System')

# Render the graph
dot.render('bloss_architecture', view=True, format='png')
import graphviz as gv

dot = gv.Digraph(name='Bytom_Architecture', 
                 comment='Bytom Server Architecture',
                 format='png')

# Configure diagram attributes
dot.attr(rankdir='TB')
dot.attr('node', shape='box', style='rounded')
dot.attr(splines='ortho')

# Add clusters/subgraphs
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Blockchain')
    core.node('protocol', 'Protocol\n(bc, types, validation)')
    core.node('txpool', 'Transaction Pool')
    core.node('consensus', 'Consensus')
    core.node('mining', 'Mining\n(Tensority)')

with dot.subgraph(name='cluster_network') as network:
    network.attr(label='Networking')
    network.node('p2p', 'P2P Network')
    network.node('netsync', 'Block Sync')
    network.node('api', 'gRPC API')

with dot.subgraph(name='cluster_storage') as storage:
    storage.attr(label='Storage')
    storage.node('db', 'Database\n(LevelDB)')
    storage.node('state', 'State Management')

with dot.subgraph(name='cluster_security') as security:
    security.attr(label='Security')
    security.node('auth', 'Access Token')
    security.node('crypto', 'Cryptography')
    security.node('hsm', 'Pseudohsm')

# Add edges
dot.edge('p2p', 'netsync')
dot.edge('netsync', 'protocol')
dot.edge('protocol', 'txpool')
dot.edge('txpool', 'mining')
dot.edge('protocol', 'db')
dot.edge('protocol', 'state')
dot.edge('api', 'auth')
dot.edge('api', 'protocol')
dot.edge('mining', 'crypto')
dot.edge('hsm', 'crypto')
dot.edge('state', 'db')

if __name__ == "__main__":
    dot.render('bytom_architecture', view=True)
from graphviz import Digraph

dot = Digraph(comment='Marlowe Starter Kit Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('frontend', 'Frontend\n(dApp Examples)')
dot.node('runtime', 'Marlowe Runtime\nServices')
dot.node('wallets', 'Wallet Integration\n(CIP30/CIP45)')
dot.node('cardano', 'Cardano Node')
dot.node('jupyter', 'Jupyter Notebooks\n(Learning Resources)')
dot.node('cli', 'Command Line Tools')
dot.node('docker', 'Docker Environment')
dot.node('nix', 'Nix Environment')
dot.node('scripts', 'Automation Scripts')
dot.node('docs', 'Documentation')

# Add connections
dot.edge('frontend', 'runtime', 'API Calls')
dot.edge('frontend', 'wallets', 'Transaction Signing')
dot.edge('runtime', 'cardano', 'Chain Interaction')
dot.edge('cli', 'runtime', 'Contract Management')
dot.edge('jupyter', 'runtime', 'Contract Examples')
dot.edge('docker', 'runtime', 'Deployment')
dot.edge('nix', 'runtime', 'Deployment')
dot.edge('scripts', 'runtime', 'Automation')
dot.edge('scripts', 'wallets', 'Wallet Management')

# Add subgraph for runtime components
with dot.subgraph(name='cluster_runtime') as c:
    c.attr(label='Marlowe Runtime Components')
    c.node('proxy', 'Proxy')
    c.node('indexer', 'Chain Indexer')
    c.node('sync', 'Chain Sync')
    c.node('tx', 'Transaction')
    c.node('web', 'Web Server')
    
    c.edge('proxy', 'indexer')
    c.edge('proxy', 'sync')
    c.edge('proxy', 'tx')
    c.edge('proxy', 'web')

dot.render('marlowe_architecture', format='png', cleanup=True)
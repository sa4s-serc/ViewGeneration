from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Marlowe Starter Kit Architecture')

# Define styles
styles = {
    'graph': {
        'label': 'Marlowe Starter Kit Architecture',
        'fontsize': '16',
        'fontcolor': 'black',
        'bgcolor': 'white',
        'rankdir': 'LR',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': 'lightgrey',
    },
    'edges': {
        'style': 'solid',
        'color': 'black',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '10',
        'fontcolor': 'black',
    }
}

dot.graph_attr.update(styles['graph'])
dot.node_attr.update(styles['nodes'])
dot.edge_attr.update(styles['edges'])

# Define nodes
dot.node('Jupyter', 'Jupyter Notebooks')
dot.node('Docker', 'Docker Environment')
dot.node('Nix', 'Nix Support')
dot.node('MarloweRuntime', 'Marlowe Runtime')
dot.node('Wallets', 'Wallet Interaction (CIP30/CIP45)')
dot.node('CLI', 'Command-Line Tools')
dot.node('Deployment', 'Deployment and Configuration')
dot.node('UI', 'UI Examples')
dot.node('Docs', 'Documentation')
dot.node('Safety', 'Safety Checks')

# Define edges
dot.edge('Jupyter', 'MarloweRuntime', label='Integrates with', dir='forward')
dot.edge('Docker', 'MarloweRuntime', label='Hosts', dir='forward')
dot.edge('Nix', 'Deployment', label='Supports', dir='forward')
dot.edge('MarloweRuntime', 'Wallets', label='Interacts with', dir='forward')
dot.edge('CLI', 'MarloweRuntime', label='Uses', dir='forward')
dot.edge('Deployment', 'Docker', label='Via Docker Compose', dir='forward')
dot.edge('UI', 'MarloweRuntime', label='Uses', dir='forward')
dot.edge('Docs', 'Deployment', label='Guides', dir='forward')
dot.edge('Safety', 'MarloweRuntime', label='Analyzes', dir='forward')

# Render the graph as a PNG
dot.render('marlowe_starter_kit_architecture', format='png', cleanup=True)
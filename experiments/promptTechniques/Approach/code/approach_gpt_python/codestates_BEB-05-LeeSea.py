from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='LeeSeaNFT Architecture')

# Define node styles
styles = {
    'smart_contract': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightgrey'},
    'frontend_component': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightblue'},
    'redux': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightgreen'},
    'web3': {'shape': 'ellipse', 'style': 'filled', 'fillcolor': 'lightyellow'},
    'yul': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightcoral'}
}

# Add nodes
dot.node('A', 'LeeSeaNFT.sol', **styles['smart_contract'])
dot.node('B', 'LeeSeaMarket.sol', **styles['smart_contract'])
dot.node('C', 'React Frontend', **styles['frontend_component'])
dot.node('D', 'Redux Store', **styles['redux'])
dot.node('E', 'Web3.js', **styles['web3'])
dot.node('F', '#utility.yul', **styles['yul'])

# Add edges
dot.edge('C', 'D', label='State Management')
dot.edge('C', 'E', label='Blockchain Interaction')
dot.edge('D', 'E', label='Async Actions')
dot.edge('E', 'A', label='Contract Calls')
dot.edge('E', 'B', label='Marketplace Calls')
dot.edge('A', 'F', label='Low-Level Functions')
dot.edge('B', 'F', label='Low-Level Functions')

# Render the diagram to a file
dot.render('leeseanft_architecture', format='png', cleanup=True)
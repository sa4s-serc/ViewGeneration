from graphviz import Digraph

# Create a new Digraph
dot = Digraph(comment='Nishu0 Anime NFT Marketplace Architecture')

# Define nodes with styles
dot.node('A', 'React/Next.js Frontend', shape='box', style='filled', color='lightblue')
dot.node('B', 'NFTContext.js', shape='box', style='filled', color='lightgrey')
dot.node('C', 'Solidity Smart Contract', shape='box', style='filled', color='lightyellow')
dot.node('D', 'IPFS Storage', shape='cylinder', style='filled', color='lightgreen')
dot.node('E', 'Metamask Wallet', shape='box', style='filled', color='lightpink')

# Define edges with styles
dot.edge('A', 'B', label='Context API', style='dashed')
dot.edge('B', 'C', label='Function calls', style='solid')
dot.edge('A', 'C', label='ABI & Contract Address', style='dotted')
dot.edge('C', 'D', label='Store Metadata', style='solid')
dot.edge('A', 'E', label='Wallet Integration', style='solid')

# Render the graph to a file
dot.render('nft_marketplace_architecture', format='png', cleanup=True)
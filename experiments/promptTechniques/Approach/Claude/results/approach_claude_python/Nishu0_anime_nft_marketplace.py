from graphviz import Digraph

dot = Digraph(comment='NFT Marketplace Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
dot.attr('edge', fontname='Arial')

# Add components
dot.node('frontend', 'Frontend\n(React/Next.js)', fillcolor='lightblue')
dot.node('context', 'NFT Context\n(State Management)', fillcolor='lightgreen')
dot.node('smart_contract', 'Smart Contract\n(Solidity)', fillcolor='lightpink')
dot.node('ipfs', 'IPFS Storage', fillcolor='lightyellow')
dot.node('blockchain', 'Blockchain\n(Ethereum/Polygon)', fillcolor='lightgrey')
dot.node('metamask', 'MetaMask Wallet', fillcolor='orange')

# Add subcomponents
with dot.subgraph(name='cluster_frontend') as c:
    c.attr(label='Frontend Components')
    c.node('pages', 'Pages\n(index, create-nft,\nmy-nfts, nft-details)')
    c.node('components', 'UI Components\n(Navbar, Cards,\nForms, Modals)')
    c.node('web3modal', 'Web3Modal')

# Add connections
dot.edge('frontend', 'context', 'State Updates')
dot.edge('context', 'smart_contract', 'Contract Interactions')
dot.edge('smart_contract', 'blockchain', 'Transactions')
dot.edge('frontend', 'ipfs', 'Store NFT Metadata')
dot.edge('metamask', 'frontend', 'Wallet Connection')
dot.edge('pages', 'components', 'Renders')
dot.edge('components', 'web3modal', 'Triggers')
dot.edge('web3modal', 'metamask', 'Connects')

# Save the diagram
dot.render('nft_marketplace_architecture', format='png', cleanup=True)
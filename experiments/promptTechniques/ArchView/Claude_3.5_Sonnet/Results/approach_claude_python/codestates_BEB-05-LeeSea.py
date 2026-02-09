from graphviz import Digraph

dot = Digraph('LeeSeaNFT Architecture', format='png')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Add main layers
with dot.subgraph(name='cluster_frontend') as frontend:
    frontend.attr(label='Frontend Layer', style='rounded', color='blue')
    frontend.node('react', 'React Components\n(Navbar, Home, Profile,\nCreate, Explore)', shape='component')
    frontend.node('redux', 'Redux Store\n(Account & Token Slices)', shape='cylinder')
    frontend.edge('redux', 'react', 'State Management')

with dot.subgraph(name='cluster_middleware') as middleware:
    middleware.attr(label='Middleware Layer', style='rounded', color='green')
    middleware.node('web3', 'Web3.js\n(Blockchain Interface)', shape='hexagon')
    middleware.node('metamask', 'MetaMask\n(Wallet Connection)', shape='doubleoctagon')

with dot.subgraph(name='cluster_blockchain') as blockchain:
    blockchain.attr(label='Blockchain Layer', style='rounded', color='red')
    blockchain.node('nft_contract', 'LeeSeaNFT.sol\n(NFT Management)', shape='component')
    blockchain.node('market_contract', 'LeeSeaMarket.sol\n(Marketplace Logic)', shape='component')
    blockchain.node('yul', '#utility.yul\n(Low-level Operations)', shape='note')
    blockchain.edge('nft_contract', 'yul', 'Uses')
    blockchain.edge('market_contract', 'yul', 'Uses')

# Connect layers
dot.edge('react', 'web3', 'API Calls')
dot.edge('web3', 'metamask', 'Wallet\nInteraction')
dot.edge('web3', 'nft_contract', 'Contract\nCalls')
dot.edge('web3', 'market_contract', 'Contract\nCalls')

# Add legend
with dot.subgraph(name='cluster_legend') as legend:
    legend.attr(label='Legend', style='rounded', color='gray')
    legend.node('comp', 'Component', shape='component')
    legend.node('store', 'Data Store', shape='cylinder')
    legend.node('interface', 'Interface', shape='hexagon')
    legend.node('wallet', 'Wallet', shape='doubleoctagon')
    legend.node('impl', 'Implementation', shape='note')

dot.render('leesea_nft_architecture', view=True, cleanup=True)
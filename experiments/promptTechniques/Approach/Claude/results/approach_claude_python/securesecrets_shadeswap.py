import graphviz

# Create a new directed graph
dot = graphviz.Digraph(
    'ShadeSwap Architecture',
    comment='ShadeSwap Smart Contract Architecture',
    engine='dot'
)

# Set graph attributes
dot.attr(rankdir='TB', splines='ortho')
dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightgray')

# Add nodes with clusters
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Core Contracts', style='rounded', color='gray')
    c.node('factory', 'Factory Contract\n(Deploys & Manages)')
    c.node('amm_pair', 'AMM Pair Contract\n(Swaps & Liquidity)')
    c.node('lp_token', 'LP Token Contract\n(SNIP-20)')
    c.node('staking', 'Staking Contract\n(Rewards & Claims)')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Supporting Contracts', style='rounded', color='gray')
    c.node('router', 'Router Contract\n(Multi-hop Swaps)')
    c.node('admin', 'Admin Contract\n(Permissions)')

# Add shared utilities node
dot.node('shared', 'Shared Utilities\n(Data Structures & Interfaces)', shape='hexagon')

# Add edges with descriptions
dot.edge('factory', 'amm_pair', 'deploys')
dot.edge('factory', 'lp_token', 'deploys')
dot.edge('amm_pair', 'lp_token', 'mints/burns')
dot.edge('lp_token', 'staking', 'stakes')
dot.edge('router', 'amm_pair', 'executes swaps')
dot.edge('admin', 'factory', 'manages')
dot.edge('admin', 'router', 'manages')

# Connect shared utilities
dot.edge('shared', 'lp_token')
dot.edge('shared', 'staking')
dot.edge('shared', 'amm_pair')
dot.edge('shared', 'factory')
dot.edge('shared', 'router')

# Render the graph
dot.render('shadeswap_architecture', format='png', cleanup=True)
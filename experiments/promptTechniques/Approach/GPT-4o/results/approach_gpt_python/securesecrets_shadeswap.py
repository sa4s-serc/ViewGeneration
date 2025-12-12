from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ShadeSwap Ecosystem Architecture', format='png')

# Define nodes for core components
dot.node('LP', 'SNIP-20 Token Implementation (lp_token)', shape='rectangle', style='filled', color='lightblue')
dot.node('ST', 'Staking Contract', shape='rectangle', style='filled', color='lightblue')
dot.node('AMM', 'AMM Pair Contract', shape='rectangle', style='filled', color='lightblue')
dot.node('FAC', 'Factory Contract', shape='rectangle', style='filled', color='lightblue')
dot.node('ROU', 'Router Contract', shape='rectangle', style='filled', color='lightblue')
dot.node('ADM', 'Admin Contract', shape='rectangle', style='filled', color='lightblue')
dot.node('SHU', 'Shared Utilities (shadeswap-shared)', shape='rectangle', style='filled', color='lightblue')

# Define edges for interactions
dot.edge('FAC', 'AMM', 'Deploys/Manages')
dot.edge('FAC', 'LP', 'Deploys/Manages')
dot.edge('ROU', 'AMM', 'Facilitates Trades')
dot.edge('ROU', 'FAC', 'Orchestrates')
dot.edge('ADM', 'FAC', 'Manages Permissions')
dot.edge('ADM', 'ROU', 'Manages Permissions')
dot.edge('AMM', 'ST', 'Manages Staking')
dot.edge('LP', 'ST', 'Staked For Rewards')
dot.edge('SHU', 'LP', 'Uses Shared Utilities')
dot.edge('SHU', 'ST', 'Uses Shared Utilities')
dot.edge('SHU', 'AMM', 'Uses Shared Utilities')
dot.edge('SHU', 'FAC', 'Uses Shared Utilities')
dot.edge('SHU', 'ROU', 'Uses Shared Utilities')
dot.edge('SHU', 'ADM', 'Uses Shared Utilities')

# Render the graph
dot.render('shadeswap_architecture')
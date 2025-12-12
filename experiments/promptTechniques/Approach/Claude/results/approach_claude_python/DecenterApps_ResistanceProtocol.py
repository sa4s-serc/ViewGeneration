import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(name='NOI_Stablecoin_Architecture', 
                 comment='NOI Stablecoin System Architecture',
                 format='png')

# Graph attributes
dot.attr(rankdir='TB', 
        splines='ortho',
        nodesep='0.8',
        ranksep='1.0')

# Node attributes
dot.attr('node', shape='box', style='rounded', fontname='Arial')

# Define clusters/subgraphs for different layers
with dot.subgraph(name='cluster_0') as frontend:
    frontend.attr(label='Frontend Layer')
    frontend.node('react_ui', 'React UI\n(CDP Management)')
    frontend.node('web3', 'Web3 Interface')

with dot.subgraph(name='cluster_1') as smart_contracts:
    smart_contracts.attr(label='Smart Contracts Layer')
    smart_contracts.node('stablecoin', 'NOI Stablecoin\nProtocol')
    smart_contracts.node('cdp_manager', 'CDP Manager')
    smart_contracts.node('price_control', 'Price Stabilization\nMechanism')
    smart_contracts.node('liquidation', 'Liquidation\nMechanism')

with dot.subgraph(name='cluster_2') as simulation:
    simulation.attr(label='Simulation Layer')
    simulation.node('sim_engine', 'Simulation Engine')
    simulation.node('agents', 'Agent Models')
    simulation.node('price_feed', 'Price Feed\nSimulation')

with dot.subgraph(name='cluster_3') as monitoring:
    monitoring.attr(label='Monitoring & Control')
    monitoring.node('pid_controller', 'PID Controllers')
    monitoring.node('events', 'Event Monitoring')
    monitoring.node('bots', 'Automation Bots')

# Add edges
dot.edge('react_ui', 'web3')
dot.edge('web3', 'stablecoin')
dot.edge('web3', 'cdp_manager')
dot.edge('stablecoin', 'price_control')
dot.edge('cdp_manager', 'liquidation')
dot.edge('price_control', 'pid_controller')
dot.edge('sim_engine', 'agents')
dot.edge('agents', 'price_feed')
dot.edge('price_feed', 'price_control')
dot.edge('events', 'bots')
dot.edge('bots', 'liquidation')
dot.edge('pid_controller', 'price_control')

# Save the diagram
dot.render('noi_stablecoin_architecture', view=True, cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='NOI Stablecoin Architecture', format='png')

# Define styles for different component types
style_layers = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#d3d3d3'}
style_packages = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#a9a9a9'}
style_components = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#f0e68c'}

# Add nodes for layers
dot.node('Frontend', 'Frontend Layer', **style_layers)
dot.node('Backend', 'Backend Layer', **style_layers)
dot.node('Simulation', 'Simulation Layer', **style_layers)
dot.node('Smart Contracts', 'Smart Contracts Layer', **style_layers)

# Add nodes for packages/components
dot.node('ReactApp', 'React Application', **style_packages)
dot.node('PythonSim', 'Python Simulation Engine', **style_packages)
dot.node('SolidityContracts', 'Solidity Smart Contracts', **style_packages)
dot.node('Deployment', 'Deployment & Monitoring Scripts', **style_packages)

# Add components within packages
dot.node('Dashboard', 'Dashboard', **style_components)
dot.node('CDPManager', 'CDP Manager', **style_components)
dot.node('PIDController', 'PID Controller', **style_components)
dot.node('LiquidationBot', 'Liquidation Bot', **style_components)

# Define connections between layers and packages
dot.edge('Frontend', 'ReactApp')
dot.edge('Backend', 'Deployment')
dot.edge('Simulation', 'PythonSim')
dot.edge('Smart Contracts', 'SolidityContracts')

# Define connections between packages and components
dot.edge('ReactApp', 'Dashboard')
dot.edge('ReactApp', 'CDPManager')
dot.edge('PythonSim', 'PIDController')
dot.edge('Deployment', 'LiquidationBot')

# Define interactions
dot.edge('CDPManager', 'SolidityContracts', label='Emits Events', style='dashed')
dot.edge('PIDController', 'SolidityContracts', label='Controls', style='dashed')
dot.edge('LiquidationBot', 'SolidityContracts', label='Monitors', style='dashed')

# Save and render the graph
dot.render('noi_stablecoin_architecture')
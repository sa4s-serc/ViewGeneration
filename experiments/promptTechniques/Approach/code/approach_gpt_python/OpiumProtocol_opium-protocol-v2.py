from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Opium Protocol v2 Architecture')

# Add nodes for key components in the Opium Protocol
dot.node('Core', 'Core Contract', shape='box', style='filled', fillcolor='lightblue')
dot.node('Registry', 'Registry Contract', shape='box', style='filled', fillcolor='lightgreen')
dot.node('SyntheticAggregator', 'Synthetic Aggregator', shape='box', style='filled', fillcolor='lightcoral')
dot.node('OracleAggregator', 'Oracle Aggregator', shape='box', style='filled', fillcolor='lightgoldenrod')
dot.node('OpiumProxyFactory', 'Opium Proxy Factory', shape='box', style='filled', fillcolor='lightgrey')
dot.node('TokenSpender', 'Token Spender', shape='box', style='filled', fillcolor='lightsalmon')

# Add edges to represent interactions and data flow
dot.edge('Registry', 'Core', label='Config & Addresses')
dot.edge('Core', 'SyntheticAggregator', label='Derivative Logic')
dot.edge('Core', 'OracleAggregator', label='Fetch Price Feeds')
dot.edge('Core', 'OpiumProxyFactory', label='Deploy Position Tokens')
dot.edge('Core', 'TokenSpender', label='Manage Token Transfers')
dot.edge('SyntheticAggregator', 'Core', label='Cache Data')
dot.edge('OracleAggregator', 'Core', label='Provide Data')
dot.edge('OpiumProxyFactory', 'Core', label='Token Creation & Burning')
dot.edge('TokenSpender', 'Core', label='Token Allowance & Transfer')

# Render the diagram
dot.render('opium_protocol_v2_architecture', format='png', cleanup=True)
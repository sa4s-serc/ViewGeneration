import graphviz

dot = graphviz.Digraph(comment='Opium Protocol v2 Architecture')
dot.attr(rankdir='TB', size='8,8')

# Registry and Core
dot.node('Registry', 'Registry\n(Central Configuration)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Core', 'Core\n(Derivative Management)', shape='rectangle', style='filled', fillcolor='lightblue')

# Aggregators
dot.node('SyntheticAggregator', 'SyntheticAggregator\n(Logic & Caching)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('OracleAggregator', 'OracleAggregator\n(Data Fetching)', shape='rectangle', style='filled', fillcolor='lightgreen')

# Factory and Tokens
dot.node('OpiumProxyFactory', 'OpiumProxyFactory\n(Token Deployment)', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('PositionTokens', 'Position Tokens\n(ERC20 LONG/SHORT)', shape='oval', style='filled', fillcolor='lightcoral')

# Security and Helpers
dot.node('TokenSpender', 'TokenSpender\n(Security Layer)', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('Helpers', 'Helper Contracts\n(Commission, Execution)', shape='rectangle', style='filled', fillcolor='lightgrey')

# Libraries
dot.node('Libraries', 'Libraries\n(LibDerivative, LibRoles)', shape='rectangle', style='filled', fillcolor='wheat')

# External Components
dot.node('Oracles', 'External Oracles', shape='cylinder', style='filled', fillcolor='white')
dot.node('Synthetics', 'Synthetic Contracts', shape='cylinder', style='filled', fillcolor='white')
dot.node('Users', 'Users/Third Parties', shape='ellipse', style='filled', fillcolor='white')

# Relationships
dot.edge('Registry', 'Core', label='Configuration', style='dashed')
dot.edge('Core', 'SyntheticAggregator', label='Logic Query')
dot.edge('Core', 'OracleAggregator', label='Data Request')
dot.edge('Core', 'OpiumProxyFactory', label='Token Creation')
dot.edge('OpiumProxyFactory', 'PositionTokens', label='Deploys')
dot.edge('Core', 'TokenSpender', label='Token Transfer')
dot.edge('Core', 'Helpers', label='Uses')
dot.edge('Core', 'Libraries', label='Imports')
dot.edge('Oracles', 'OracleAggregator', label='Feeds Data')
dot.edge('Synthetics', 'SyntheticAggregator', label='Provides Logic')
dot.edge('Users', 'Core', label='Interacts')

dot.render('opium_protocol_architecture', format='png', cleanup=True)
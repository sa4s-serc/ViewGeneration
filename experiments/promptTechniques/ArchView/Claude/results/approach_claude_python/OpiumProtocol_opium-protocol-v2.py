from graphviz import Digraph

dot = Digraph(comment='Opium Protocol v2 Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('core', 'Core\n(Position Creation, Margin, Payouts)')
dot.node('synth_agg', 'Synthetic Aggregator\n(Derivative Logic & Data Cache)')
dot.node('oracle_agg', 'Oracle Aggregator\n(Price Feeds & Data Cache)')
dot.node('proxy_factory', 'Opium Proxy Factory\n(Position Token Deployment)')
dot.node('registry', 'Registry\n(Contract Addresses & Parameters)')
dot.node('token_spender', 'Token Spender\n(ERC20 Transfer Management)')

# Add position tokens
dot.node('long_token', 'Long Position Token\n(ERC20)')
dot.node('short_token', 'Short Position Token\n(ERC20)')

# Define edges
dot.edge('registry', 'core', 'Configures')
dot.edge('registry', 'synth_agg', 'Configures')
dot.edge('registry', 'oracle_agg', 'Configures')
dot.edge('registry', 'token_spender', 'Whitelists')

dot.edge('core', 'synth_agg', 'Fetches derivative data')
dot.edge('core', 'oracle_agg', 'Fetches price data')
dot.edge('core', 'proxy_factory', 'Creates positions')
dot.edge('core', 'token_spender', 'Manages transfers')

dot.edge('proxy_factory', 'long_token', 'Deploys')
dot.edge('proxy_factory', 'short_token', 'Deploys')

# Render the diagram
dot.render('opium_protocol_architecture', view=True, format='png')
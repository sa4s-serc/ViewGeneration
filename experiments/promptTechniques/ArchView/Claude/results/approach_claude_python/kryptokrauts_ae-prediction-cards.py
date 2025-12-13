from graphviz import Digraph

dot = Digraph(comment='Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('frontend', 'Frontend\n(React)')
dot.node('smartcontract', 'Smart Contract\n(Aeternity)')
dot.node('oracle', 'Oracle Service\n(Java)')
dot.node('prediction', 'Prediction Service\n(Java)')
dot.node('blockchain', 'Aeternity\nBlockchain')

# Add subgraph for backend services
with dot.subgraph(name='cluster_backend') as backend:
    backend.attr(label='Backend Services')
    backend.attr('node', style='filled', fillcolor='lightgrey')
    backend.node('oracle_internal', 'Oracle Service')
    backend.node('prediction_internal', 'Prediction Service')

# Add connections
dot.edge('frontend', 'smartcontract', 'Interact')
dot.edge('smartcontract', 'blockchain', 'Deploy/Execute')
dot.edge('oracle', 'blockchain', 'Query/Response')
dot.edge('prediction', 'blockchain', 'Monitor/Process')
dot.edge('oracle', 'smartcontract', 'Provide Price Data')
dot.edge('prediction', 'smartcontract', 'Process Results')

# Save the diagram
dot.render('architecture_view', format='png', cleanup=True)
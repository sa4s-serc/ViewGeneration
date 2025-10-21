from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='2WAY_Design Architecture')

# Define node styles
node_styles = {
    'style': 'filled',
    'fillcolor': 'lightgrey',
    'fontname': 'Helvetica'
}

# Define edge styles
edge_styles = {
    'color': 'black',
    'fontname': 'Helvetica'
}

# Add nodes with specific shapes
dot.node('A', 'Trust Network', shape='rect', **node_styles)
dot.node('B', 'Authorization & Authentication', shape='rect', **node_styles)
dot.node('C', 'Data Exchange Module', shape='rect', **node_styles)
dot.node('D', 'Differential Privacy', shape='rect', **node_styles)
dot.node('E', 'Private Data Storage', shape='cylinder', fillcolor='lightblue', style='filled', fontname='Helvetica')
dot.node('F', 'API Gateway', shape='parallelogram', fillcolor='lightgreen', style='filled', fontname='Helvetica')

# Add edges
dot.edge('A', 'B', label='Establish Trust', **edge_styles)
dot.edge('B', 'C', label='Secure Data Transfer', **edge_styles)
dot.edge('C', 'D', label='Privacy Techniques', **edge_styles)
dot.edge('D', 'A', label='Feedback Loop', **edge_styles)
dot.edge('C', 'E', label='Store & Retrieve', **edge_styles)
dot.edge('F', 'C', label='API Calls', **edge_styles)
dot.edge('E', 'F', label='Data Access', **edge_styles)

# Render the diagram
dot.render('2WAY_Design_Architecture', format='png', cleanup=True)
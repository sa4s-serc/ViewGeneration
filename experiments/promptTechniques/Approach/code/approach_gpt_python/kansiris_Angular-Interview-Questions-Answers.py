from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Angular Interview Questions and Answers Architecture')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgrey')

# Add nodes for components
dot.node('Q&A', 'Extensive Q&A Collection')
dot.node('Code', 'Code Examples')
dot.node('Nav', 'Navigation')
dot.node('LIC', 'Licensing')

# Add nodes for architectural insights
dot.node('Modular', 'Modular Content Organization')
dot.node('Practical', 'Practical Application Focus')
dot.node('Coverage', 'Broad Coverage of Angular Concepts')
dot.node('RepoPattern', 'Knowledge Repository Pattern')

# Add edges for data flow
dot.edge('Q&A', 'Code', label='includes')
dot.edge('Q&A', 'Nav', label='structured in')
dot.edge('Nav', 'LIC', label='linked to')

# Add edges for architectural insights
dot.edge('Modular', 'Q&A', label='facilitates updates')
dot.edge('Practical', 'Code', label='enhances understanding')
dot.edge('Coverage', 'Q&A', label='covers spectrum')
dot.edge('RepoPattern', 'Q&A', label='centralizes info')

# Render the graph
dot.render('angular_architecture_diagram', format='png', cleanup=True)
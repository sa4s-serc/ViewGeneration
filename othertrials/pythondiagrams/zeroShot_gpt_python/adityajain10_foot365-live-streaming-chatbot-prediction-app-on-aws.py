import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Architectural View Diagram')

# Add nodes based on Components Nature
dot.node('A', 'Service A', shape='box', style='filled', fillcolor='lightblue')
dot.node('B', 'Service B', shape='box', style='filled', fillcolor='lightgreen')
dot.node('C', 'Database', shape='cylinder', style='filled', fillcolor='lightgrey')

# Add edges based on Connectors Nature and Connectors Direction
dot.edge('A', 'B', label='REST API', arrowhead='normal')
dot.edge('B', 'C', label='SQL Query', arrowhead='normal')

# Render the diagram to a file
dot.render('architectural_view_diagram', format='png', cleanup=True)
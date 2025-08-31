from graphviz import Digraph

# Initialize a directed graph
dot = Digraph(comment='Software Architecture')

# Define the nodes based on component nature
dot.node('A', 'Service A', shape='rectangle', style='filled', color='lightblue')
dot.node('B', 'Service B', shape='rectangle', style='filled', color='lightgreen')
dot.node('C', 'API Gateway', shape='rectangle', style='filled', color='lightcoral')

# Define edges based on connectors nature and direction
dot.edge('A', 'C', 'REST API', arrowhead='normal')
dot.edge('B', 'C', 'REST API', arrowhead='normal')

# Add a legend
with dot.subgraph(name='cluster_legend') as c:
    c.attr(label='Legend', fontsize='12')
    c.node_attr.update(shape='plaintext')
    c.node('L1', 'Service: Rectangle\nAPI: Arrow')

# Render the graph to a file
dot.render('architecture_diagram', format='png', cleanup=True)
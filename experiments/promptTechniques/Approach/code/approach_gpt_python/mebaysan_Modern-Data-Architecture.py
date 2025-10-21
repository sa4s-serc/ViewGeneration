from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Modern Data Architecture', format='png')

# Define nodes for each component
dot.node('A', 'Airbyte', shape='rectangle', style='filled', color='lightblue')
dot.node('P', 'PostgreSQL', shape='rectangle', style='filled', color='lightgreen')
dot.node('D', 'DBT', shape='rectangle', style='filled', color='lightcoral')
dot.node('S', 'Superset', shape='rectangle', style='filled', color='lightyellow')
dot.node('N', 'Nginx', shape='rectangle', style='filled', color='lightgrey')
dot.node('PS', 'Python Script', shape='rectangle', style='filled', color='lightcyan')

# Define edges for data flow and connections
dot.edge('A', 'P', label='Ingest Data', arrowhead='vee')
dot.edge('PS', 'P', label='Load CSV', arrowhead='vee')
dot.edge('P', 'D', label='Transform Data', arrowhead='vee')
dot.edge('D', 'S', label='Visualize Data', arrowhead='vee')
dot.edge('P', 'N', label='Proxy Access', arrowhead='vee')

# Define subgraph for Docker components
with dot.subgraph(name='cluster_docker') as c:
    c.attr(style='dashed', color='black')
    c.node_attr.update(style='filled', color='white')
    c.node('A')
    c.node('P')
    c.node('D')
    c.node('S')
    c.attr(label='Dockerized Components')

# Render the graph to a file
dot.render('modern_data_architecture')
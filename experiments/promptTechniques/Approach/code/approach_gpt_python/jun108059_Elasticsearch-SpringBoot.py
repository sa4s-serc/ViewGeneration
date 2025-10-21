from graphviz import Digraph

# Create a Digraph object for the architecture diagram
dot = Digraph(comment='Elasticsearch-SpringBoot Repository Architecture')

# Define the styles for different layers and systems
with dot.subgraph(name='cluster_0') as c:
    c.attr(style='filled', color='lightgrey')
    c.node_attr.update(style='filled', color='white')
    c.attr(label='Controller Layer')
    c.node('Controller', 'Spring MVC Controllers')

with dot.subgraph(name='cluster_1') as c:
    c.attr(style='filled', color='lightblue')
    c.node_attr.update(style='filled', color='white')
    c.attr(label='Service Layer')
    c.node('Service', 'Core Business Logic')

with dot.subgraph(name='cluster_2') as c:
    c.attr(style='filled', color='lightgreen')
    c.node_attr.update(style='filled', color='white')
    c.attr(label='Repository Layer')
    c.node('Repository', 'Data Access Operations')

with dot.subgraph(name='cluster_3') as c:
    c.attr(style='filled', color='salmon')
    c.node_attr.update(style='filled', color='white')
    c.attr(label='Elasticsearch Client Layer')
    c.node('Elasticsearch Client', 'Elasticsearch Interactions')

# Define additional nodes and edges for databases and configuration
dot.node('MySQL DB', 'MySQL Database', shape='cylinder', style='filled', color='lightyellow')
dot.node('Elasticsearch', 'Elasticsearch', shape='cylinder', style='filled', color='lightyellow')
dot.node('Config', 'Application Configuration', shape='folder', style='filled', color='lightcoral')

# Define connections between nodes
dot.edge('Controller', 'Service', label='calls')
dot.edge('Service', 'Repository', label='queries')
dot.edge('Repository', 'MySQL DB', label='accesses')
dot.edge('Service', 'Elasticsearch Client', label='uses')
dot.edge('Elasticsearch Client', 'Elasticsearch', label='connects')
dot.edge('Controller', 'Config', label='loads')
dot.edge('Elasticsearch Client', 'Config', label='loads')

# Save the diagram source and render the diagram
dot.render('elasticsearch_springboot_architecture', format='png', cleanup=True)
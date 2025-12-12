from graphviz import Digraph

# Creating a new directed graph
dot = Digraph(comment='FEC ERegulations Architecture')

# Adding nodes for the main components of the architecture
dot.node('DjangoApp', 'Django Application', shape='rectangle', style='filled', color='lightblue')
dot.node('PostgreSQL', 'PostgreSQL Database', shape='cylinder', style='filled', color='lightgreen')
dot.node('ElasticSearch', 'ElasticSearch', shape='ellipse', style='filled', color='lightyellow')
dot.node('CloudFoundry', 'Cloud Foundry', shape='rectangle', style='filled', color='lightgrey')
dot.node('Frontend', 'Frontend Interface', shape='rectangle', style='filled', color='lightpink')
dot.node('CMS', 'Content Management System', shape='rectangle', style='filled', color='lightcoral')

# Adding edges to represent communication paths and data flows
dot.edge('DjangoApp', 'PostgreSQL', label='stores/retrieves data', dir='both')
dot.edge('DjangoApp', 'ElasticSearch', label='search queries', dir='both')
dot.edge('DjangoApp', 'CloudFoundry', label='deploys to', dir='forward')
dot.edge('Frontend', 'DjangoApp', label='API calls', dir='forward')
dot.edge('Frontend', 'CMS', label='fetches content from', dir='forward')

# Visualizing maintainability through color coding
dot.attr('node', shape='note', color='black')
dot.node('Maintainability', 'Maintainability: Modular & Extensible\nCloud-Native, Automated Deployment', shape='note')

# Adding a legend
dot.node('Legend', 'Legend:\nRectangle: Component\nEllipse: Service\nCylinder: Database\nColor Coding: indicates different layers and responsibilities', shape='note')

# Outputting the graph to a file
dot.render('fec_eregs_architecture_diagram', format='png', cleanup=True)
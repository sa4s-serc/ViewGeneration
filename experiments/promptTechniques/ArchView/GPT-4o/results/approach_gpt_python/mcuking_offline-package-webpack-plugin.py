from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Offline Package Webpack Plugin Architecture')

# Define nodes
dot.node('A', 'OfflinePackagePlugin', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'webpack', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('C', 'jszip', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('D', 'mime-types', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('E', 'lodash', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('F', 'index.json', shape='rectangle', style='filled', fillcolor='lightgreen')

# Define edges
dot.edge('A', 'B', 'emit hook')
dot.edge('A', 'C', 'zip creation')
dot.edge('A', 'D', 'MIME detection')
dot.edge('A', 'E', 'Utility functions')
dot.edge('A', 'F', 'generate')

# Render the diagram to a file
dot.render('offline_package_webpack_plugin_architecture', format='png', cleanup=True)
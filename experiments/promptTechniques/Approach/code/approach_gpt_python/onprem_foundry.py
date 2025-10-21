from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Foundry System Architecture')

# Define nodes for components
dot.node('Furnace', 'Furnace Component', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('gRPC', 'gRPC Interface', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('pkgMap', 'pkgMap', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Metrics', 'Metrics & Health Checks', shape='rectangle', style='filled', fillcolor='yellow')
dot.node('ObjectStorage', 'Object Storage', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('Builder', 'Builder Interface', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('MakepkgBuilder', 'MakepkgBuilder', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('BuilderWithMetrics', 'BuilderWithMetrics', shape='rectangle', style='filled', fillcolor='lightcoral')

# Define edges for interactions
dot.edge('Furnace', 'gRPC', label='exposes')
dot.edge('Furnace', 'pkgMap', label='tracks')
dot.edge('Furnace', 'Metrics', label='provides')
dot.edge('Furnace', 'ObjectStorage', label='uploads to')
dot.edge('Furnace', 'Builder', label='uses')
dot.edge('Builder', 'MakepkgBuilder', label='implements')
dot.edge('Builder', 'BuilderWithMetrics', label='decorates')

# Render the graph
dot.render('foundry_architecture', format='png', cleanup=False)
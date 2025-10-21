from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='FudanOCR Architecture', format='png')

# Define nodes with different shapes and styles
dot.node('TD', 'Text Detection', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('TR', 'Text Recognition', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('SR', 'Super-Resolution', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('DH', 'Data Handling', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('MTE', 'Model Training & Evaluation', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('PP', 'Post-processing', shape='rectangle', style='filled', fillcolor='wheat')
dot.node('CO', 'Custom Operations', shape='rectangle', style='filled', fillcolor='lightpink')

# Define edges with styles
dot.edge('TD', 'TR', label='pipeline', dir='forward')
dot.edge('TR', 'SR', label='enhance', dir='forward')
dot.edge('DH', 'TD', label='data provision', dir='forward')
dot.edge('DH', 'TR', label='data provision', dir='forward')
dot.edge('DH', 'SR', label='data provision', dir='forward')
dot.edge('MTE', 'TD', label='training', dir='none')
dot.edge('MTE', 'TR', label='training', dir='none')
dot.edge('MTE', 'SR', label='training', dir='none')
dot.edge('PP', 'TD', label='post-process', dir='none')
dot.edge('PP', 'TR', label='post-process', dir='none')
dot.edge('CO', 'MTE', label='custom layers', dir='forward')
dot.edge('CO', 'PP', label='custom layers', dir='forward')

# Render the graph to a file
dot.render('fudanocr_architecture', view=True)
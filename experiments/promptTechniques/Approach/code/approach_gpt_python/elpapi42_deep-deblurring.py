from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ElPapi42 Deep Deblurring Architecture', format='png')
dot.attr(rankdir='LR', size='8,5')

# Define nodes for each component
dot.node('Frontend', 'Frontend\n(Vue.js)', shape='rect', style='filled', fillcolor='lightblue')
dot.node('Backend', 'Backend\n(Flask)', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('ModelServing', 'Model Serving\n(Tensorflow Serving)', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('ModelRepo', 'Model Repository', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('DataStorage', 'Data Storage\n(Cloudinary)', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('Redis', 'Redis\n(Caching & Session)', shape='rect', style='filled', fillcolor='lightpink')
dot.node('PostgreSQL', 'PostgreSQL\n(Database)', shape='rect', style='filled', fillcolor='lightcyan')

# Define edges for interaction
dot.edge('Frontend', 'Backend', label='REST API', arrowhead='vee')
dot.edge('Backend', 'ModelServing', label='REST API', arrowhead='vee')
dot.edge('Backend', 'ModelRepo', label='Access', arrowhead='vee')
dot.edge('Backend', 'DataStorage', label='Assets', arrowhead='vee')
dot.edge('Backend', 'Redis', label='Cache & Session', arrowhead='vee')
dot.edge('Backend', 'PostgreSQL', label='Data', arrowhead='vee')

# Save and render the graph
dot.render('el_papi42_deep_deblurring_architecture', view=True)
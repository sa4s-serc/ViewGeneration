from graphviz import Digraph

dot = Digraph(comment='ElPapi42_deep-deblurring Architecture')

# Frontend
dot.node('Frontend', 'Frontend (Vue.js)', shape='rect', style='filled', fillcolor='lightblue')

# Backend
dot.node('Backend', 'Backend (Flask)', shape='rect', style='filled', fillcolor='lightgreen')

# Model Serving
dot.node('ModelServing', 'Model Serving (TensorFlow Serving)', shape='rect', style='filled', fillcolor='lightyellow')

# Model Repository
dot.node('ModelRepo', 'Model Repository', shape='rect', style='filled', fillcolor='lightcoral')

# Data Storage
dot.node('DataStorage', 'Data Storage (Cloudinary)', shape='rect', style='filled', fillcolor='lightgrey')

# Redis
dot.node('Redis', 'Redis', shape='rect', style='filled', fillcolor='lightpink')

# PostgreSQL
dot.node('PostgreSQL', 'PostgreSQL', shape='rect', style='filled', fillcolor='lightgoldenrod')

# Edges
dot.edge('Frontend', 'Backend', label='REST API')
dot.edge('Backend', 'ModelServing', label='gRPC')
dot.edge('Backend', 'ModelRepo', label='REST API')
dot.edge('Backend', 'DataStorage', label='HTTP')
dot.edge('Backend', 'Redis', label='Caching')
dot.edge('Backend', 'PostgreSQL', label='DB Access')

# Render the graph
dot.render('elpapi42_deep_deblurring_architecture', format='png', cleanup=True)
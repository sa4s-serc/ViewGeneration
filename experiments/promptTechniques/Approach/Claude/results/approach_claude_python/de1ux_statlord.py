from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Statlord Dashboard Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('dashboard_editor', 'Dashboard Editor\n(React, Redux, Fabric.js)', shape='rectangle')
dot.node('data_viz', 'Data Visualization\n(Gauges)', shape='rectangle') 
dot.node('display_mgmt', 'Display Management', shape='rectangle')
dot.node('layout_mgmt', 'Layout Management', shape='rectangle')
dot.node('data_stream', 'Data Streaming', shape='rectangle')
dot.node('display_render', 'Display Rendering', shape='rectangle')
dot.node('api', 'API\n(Django REST Framework)', shape='rectangle')
dot.node('db', 'Database\n(PostgreSQL)', shape='cylinder')

# Add edges
dot.edge('dashboard_editor', 'layout_mgmt', 'Save Layout')
dot.edge('layout_mgmt', 'api', 'Store')
dot.edge('api', 'db', 'Persist')
dot.edge('data_stream', 'api', 'Update Data')
dot.edge('api', 'display_mgmt', 'Configure')
dot.edge('display_mgmt', 'display_render', 'Push to Display')
dot.edge('layout_mgmt', 'display_render', 'Layout Definition')
dot.edge('data_viz', 'display_render', 'Render Elements')

# Set graph attributes
dot.attr(label='Statlord Dashboard Architecture\nClient-Server Architecture with HTTP Communication')
dot.attr(fontsize='16')

# Render the graph
dot.render('statlord_architecture', format='png', cleanup=True)
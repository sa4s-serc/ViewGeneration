from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Apache NiFi/Orchsym Runtime Architecture')

# Define nodes
dot.node('A', 'FlowController', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'ProcessSession', shape='rectangle')
dot.node('C', 'FlowFile', shape='rectangle')
dot.node('D', 'Connection', shape='rectangle')
dot.node('E', 'ProcessScheduler', shape='rectangle')
dot.node('F', 'FlowFile Repository', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('G', 'Content Repository', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('H', 'Provenance Repository', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('I', 'ControllerServiceProvider', shape='rectangle')
dot.node('J', 'REST API', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('K', 'Site-to-Site Data Transfer', shape='rectangle')
dot.node('L', 'User Interface', shape='rectangle')
dot.node('M', 'Security', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('N', 'NAR Bundles', shape='rectangle')
dot.node('O', 'Cluster Coordinator', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('P', 'ZooKeeper', shape='rectangle')
dot.node('Q', 'Orchsym Branding Extension', shape='rectangle')

# Define edges
dot.edge('A', 'B', label='Manages', style='dashed')
dot.edge('A', 'C', label='Uses', style='dashed')
dot.edge('A', 'D', label='Connects', style='dashed')
dot.edge('A', 'E', label='Schedules', style='dashed')
dot.edge('F', 'C', label='Stores', style='dotted')
dot.edge('G', 'C', label='Stores', style='dotted')
dot.edge('H', 'C', label='Tracks', style='dotted')
dot.edge('I', 'A', label='Provides Services', style='dashed')
dot.edge('J', 'A', label='Exposes API', style='dashed')
dot.edge('K', 'A', label='Transfers Data', style='dashed')
dot.edge('L', 'A', label='UI Interaction', style='dashed')
dot.edge('M', 'A', label='Secures', style='dashed')
dot.edge('N', 'A', label='Extends', style='dashed')
dot.edge('O', 'P', label='Coordinates', style='dashed')
dot.edge('O', 'A', label='Manages Cluster', style='dashed')
dot.edge('Q', 'A', label='Customizes', style='dashed')

# Render the diagram to a file
dot.render('nifi_orchsym_architecture', format='png', cleanup=True)
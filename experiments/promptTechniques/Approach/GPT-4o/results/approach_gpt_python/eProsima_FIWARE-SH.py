from graphviz import Digraph

dot = Digraph(comment='FIWARE System Handle for Integration Service')

# Set graph attributes
dot.attr(rankdir='TB', size='8,5')

# Define nodes representing the key components
dot.node('SH', 'System Handle', shape='rectangle', style='filled', color='lightgrey')
dot.node('NGSIv2', 'NGSIv2 Connector', shape='rectangle', style='filled', color='lightblue')
dot.node('Listener', 'Listener', shape='rectangle', style='filled', color='lightgreen')
dot.node('Pub', 'Publisher', shape='rectangle', style='filled', color='lightcoral')
dot.node('Sub', 'Subscriber', shape='rectangle', style='filled', color='lightgoldenrod')
dot.node('FIWARE', 'FIWARE Context Broker', shape='rectangle', style='filled', color='lightyellow')
dot.node('IS', 'Integration Service', shape='rectangle', style='filled', color='lightpink')

# Define connections between nodes
dot.edge('SH', 'NGSIv2', label='configure/connect')
dot.edge('NGSIv2', 'FIWARE', label='NGSIv2 API')
dot.edge('Listener', 'NGSIv2', label='notify')
dot.edge('Pub', 'NGSIv2', label='publish')
dot.edge('Sub', 'NGSIv2', label='subscribe')
dot.edge('SH', 'Listener', label='manage')
dot.edge('SH', 'Pub', label='create')
dot.edge('SH', 'Sub', label='create')
dot.edge('IS', 'SH', label='register')

# Render the diagram
dot.render('fiware_system_handle_diagram', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='NASA cFS Architecture')

# Set graph attributes
dot.attr(rankdir='LR', size='10', style='filled', color='lightgrey')

# Define nodes (components)
dot.node('cFE', 'cFE (Core Flight Executive)', shape='rectangle', style='filled', color='lightblue')
dot.node('OSAL', 'OSAL (Operating System Abstraction Layer)', shape='rectangle', style='filled', color='lightgreen')
dot.node('PSP', 'PSP (Platform Support Package)', shape='rectangle', style='filled', color='lightyellow')
dot.node('Apps', 'Applications', shape='rectangle', style='filled', color='lightpink')
dot.node('Tools', 'Tools', shape='rectangle', style='filled', color='lightcoral')
dot.node('ES', 'Event Services', shape='rectangle', style='filled', color='lightcyan')

# Add edges (connectors)
dot.edge('cFE', 'OSAL', label='Abstraction')
dot.edge('cFE', 'PSP', label='Microkernel')
dot.edge('cFE', 'Apps', label='Component-Based')
dot.edge('cFE', 'Tools', label='Tools Integration')
dot.edge('cFE', 'ES', label='Event-Driven')

# Add a legend
dot.node('Legend', label='Legend:\n- cFE: Core Flight Executive\n- OSAL: Operating System Abstraction Layer\n- PSP: Platform Support Package\n- Apps: Applications\n- Tools: Tools\n- ES: Event Services', shape='note')

# Render the diagram
dot.render('nasa_cfs_architecture', format='png', cleanup=True)
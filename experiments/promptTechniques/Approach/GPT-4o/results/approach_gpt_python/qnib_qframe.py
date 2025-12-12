from graphviz import Digraph

# Initialize the Digraph
dot = Digraph(comment='qnib_qframe Architectural View')

# Define the core components
dot.node('C', 'Collectors', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F', 'Filters', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('H', 'Handlers', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('QC', 'QChan', shape='ellipse', style='filled', fillcolor='yellow')

# Define additional components
dot.node('YAML', 'YAML Configuration', shape='parallelogram', style='filled', fillcolor='lightgrey')
dot.node('Sys', 'System Call Abstractions', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('Sec', 'Security Mechanisms', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('Gen', 'Code Generation', shape='ellipse', style='filled', fillcolor='lightcyan')

# Define the connections (data flow)
dot.edges(['CQ', 'FQ', 'HQ'])  # Data flow through QChan
dot.edge('YAML', 'C', label='Configures', style='dashed')
dot.edge('YAML', 'F', label='Configures', style='dashed')
dot.edge('YAML', 'H', label='Configures', style='dashed')
dot.edge('Sys', 'C', label='System Interaction', style='dotted')
dot.edge('Sys', 'H', label='System Interaction', style='dotted')
dot.edge('Sec', 'C', label='Security', style='dotted')
dot.edge('Sec', 'F', label='Security', style='dotted')
dot.edge('Sec', 'H', label='Security', style='dotted')
dot.edge('Gen', 'Sys', label='Generates', style='dashed')

# Render the diagram to a file
dot.render('qnib_qframe_architecture', format='png', cleanup=True)
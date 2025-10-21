from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Crux Cross-Platform Development Framework', format='png')

# Add nodes for core components
dot.node('1', 'App Trait', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('2', 'Core Struct', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('3', 'Effect Trait', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('4', 'Bridge Struct', shape='rectangle', style='filled', fillcolor='lightblue')

# Add nodes for capabilities
dot.node('5', 'Capabilities', shape='ellipse', style='filled', fillcolor='lightgreen')
dot.node('6', 'Command', shape='ellipse', style='filled', fillcolor='lightgreen')

# Add nodes for utilities
dot.node('7', 'crux_http', shape='cylinder', style='filled', fillcolor='lightyellow')
dot.node('8', 'crux_time', shape='cylinder', style='filled', fillcolor='lightyellow')

# Add nodes for architectural patterns
dot.node('9', 'Ports & Adapters', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('10', 'MVU', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('11', 'Event Sourcing', shape='ellipse', style='filled', fillcolor='lightcoral')

# Add edges to represent relationships
dot.edge('1', '2', label='defines structure', arrowhead='open')
dot.edge('2', '3', label='requests', arrowhead='open')
dot.edge('3', '4', label='communicates with', arrowhead='open')
dot.edge('5', '6', label='uses', arrowhead='open')
dot.edge('6', '3', label='encapsulates', arrowhead='open')
dot.edge('7', '5', label='HTTP requests', arrowhead='open')
dot.edge('8', '5', label='Time requests', arrowhead='open')
dot.edge('9', '1', label='applies', arrowhead='open')
dot.edge('10', '1', label='influences', arrowhead='open')
dot.edge('11', '2', label='updates state', arrowhead='open')

# Render the graph to a file
dot.render('crux_architecture_diagram')
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='CodeMirror and ComPar Architectural Diagram')

# Define nodes representing key components and functionalities
dot.node('CM', 'CodeMirror')
dot.node('ComP', 'ComPar')
dot.node('Core', 'Core Editor Functionality')
dot.node('Lang', 'Language Modes')
dot.node('Key', 'Keymaps')
dot.node('Addons', 'Addons')
dot.node('GUI', 'GUI Framework')
dot.node('Comp', 'Compiler Abstraction')
dot.node('Tools', 'Parallelization Tools Integration')
dot.node('Params', 'Compilation Parameter Combinations')
dot.node('DB', 'Database Interaction (MongoDB)')
dot.node('RT', 'Runtime Analysis')

# Define additional components
dot.node('Doc', 'Document Management')
dot.node('Hist', 'History Management')
dot.node('Event', 'Event Handling')
dot.node('Input', 'Input Methods')

# Define relationships (edges) between components
# CodeMirror components
dot.edge('CM', 'Core')
dot.edge('CM', 'Lang')
dot.edge('CM', 'Key')
dot.edge('CM', 'Addons')
dot.edge('Core', 'Doc')
dot.edge('Core', 'Hist')
dot.edge('Core', 'Event')
dot.edge('Core', 'Input')

# ComPar components
dot.edge('ComP', 'GUI')
dot.edge('ComP', 'Comp')
dot.edge('ComP', 'Tools')
dot.edge('ComP', 'Params')
dot.edge('ComP', 'DB')
dot.edge('ComP', 'RT')

# Define node styles
dot.node('CM', shape='rectangle', style='filled', color='lightblue')
dot.node('ComP', shape='rectangle', style='filled', color='lightgreen')

# Define edge styles
dot.edge('CM', 'Core', style='dashed', color='blue')
dot.edge('ComP', 'GUI', style='dashed', color='green')

# Render the graph to a file and view it
dot.render('architecture_diagram', format='png', cleanup=True)
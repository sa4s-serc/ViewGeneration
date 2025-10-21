from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Visual Programming Environment Architecture')

# Define nodes for each major component
dot.node('SR', 'Syntax Representation', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('EE', 'Execution Engine', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('L', 'Library', shape='rectangle', style='filled', fillcolor='lightyellow')

# Define subcomponents for Syntax Representation
dot.node('SR1', 'Element API', shape='rect', style='filled', fillcolor='lightblue')
dot.node('SR2', 'Specification', shape='rect', style='filled', fillcolor='lightblue')
dot.node('SR3', 'Warehouse', shape='rect', style='filled', fillcolor='lightblue')
dot.node('SR4', 'Syntax Tree', shape='rect', style='filled', fillcolor='lightblue')

# Define subcomponents for Execution Engine
dot.node('EE1', 'Symbol Table', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('EE2', 'Parser', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('EE3', 'Interpreter', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('EE4', 'Scheduler', shape='rect', style='filled', fillcolor='lightgreen')

# Define subcomponents for Library
dot.node('L1', 'Values', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('L2', 'Boxes and Box Identifiers', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('L3', 'Math Operators', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('L4', 'Conditionals', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('L5', 'Loops', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('L6', 'Program Structures', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('L7', 'Miscellaneous', shape='rect', style='filled', fillcolor='lightyellow')

# Define edges for subcomponents in Syntax Representation
dot.edge('SR', 'SR1')
dot.edge('SR', 'SR2')
dot.edge('SR', 'SR3')
dot.edge('SR', 'SR4')

# Define edges for subcomponents in Execution Engine
dot.edge('EE', 'EE1')
dot.edge('EE', 'EE2')
dot.edge('EE', 'EE3')
dot.edge('EE', 'EE4')

# Define edges for subcomponents in Library
dot.edge('L', 'L1')
dot.edge('L', 'L2')
dot.edge('L', 'L3')
dot.edge('L', 'L4')
dot.edge('L', 'L5')
dot.edge('L', 'L6')
dot.edge('L', 'L7')

# Define relationships between major components
dot.edge('SR4', 'EE2', 'parses')
dot.edge('EE2', 'EE3', 'executes')
dot.edge('EE3', 'EE4', 'schedules')
dot.edge('SR3', 'SR4', 'manages instances')
dot.edge('SR2', 'SR3', 'manages specifications')
dot.edge('L', 'SR', 'provides elements')

# Save the source code and render the graph
dot.render('visual_programming_environment_architecture', view=True)
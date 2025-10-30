from graphviz import Digraph

def generate_architecture_diagram():
    dot = Digraph(comment='Visual Programming Environment Library Architecture')

    # Define components
    dot.node('SR', 'Syntax Representation', shape='rectangle', style='filled', color='lightblue')
    dot.node('EE', 'Execution Engine', shape='rectangle', style='filled', color='lightgreen')
    dot.node('LIB', 'Library', shape='rectangle', style='filled', color='lightcoral')

    # Define sub-components for Syntax Representation
    dot.node('SR1', 'Element API', shape='rectangle')
    dot.node('SR2', 'Specification', shape='rectangle')
    dot.node('SR3', 'Warehouse', shape='rectangle')
    dot.node('SR4', 'Syntax Tree', shape='rectangle')

    # Define sub-components for Execution Engine
    dot.node('EE1', 'Symbol Table', shape='rectangle')
    dot.node('EE2', 'Parser', shape='rectangle')
    dot.node('EE3', 'Interpreter', shape='rectangle')
    dot.node('EE4', 'Scheduler', shape='rectangle')

    # Define sub-components for Library
    dot.node('LIB1', 'Values', shape='rectangle')
    dot.node('LIB2', 'Boxes and Identifiers', shape='rectangle')
    dot.node('LIB3', 'Math Operators', shape='rectangle')
    dot.node('LIB4', 'Conditionals', shape='rectangle')
    dot.node('LIB5', 'Loops', shape='rectangle')
    dot.node('LIB6', 'Program Structures', shape='rectangle')
    dot.node('LIB7', 'Miscellaneous', shape='rectangle')

    # Create edges for Syntax Representation
    dot.edge('SR', 'SR1')
    dot.edge('SR', 'SR2')
    dot.edge('SR', 'SR3')
    dot.edge('SR', 'SR4')

    # Create edges for Execution Engine
    dot.edge('EE', 'EE1')
    dot.edge('EE', 'EE2')
    dot.edge('EE', 'EE3')
    dot.edge('EE', 'EE4')

    # Create edges for Library
    dot.edge('LIB', 'LIB1')
    dot.edge('LIB', 'LIB2')
    dot.edge('LIB', 'LIB3')
    dot.edge('LIB', 'LIB4')
    dot.edge('LIB', 'LIB5')
    dot.edge('LIB', 'LIB6')
    dot.edge('LIB', 'LIB7')

    # Define interactions
    dot.edge('SR4', 'EE2', label='Parse')
    dot.edge('EE3', 'SR3', label='Execute')
    dot.edge('EE4', 'EE3', label='Schedule')

    # Save the diagram
    dot.render('visual_programming_environment_architecture', format='png', cleanup=True)

generate_architecture_diagram()
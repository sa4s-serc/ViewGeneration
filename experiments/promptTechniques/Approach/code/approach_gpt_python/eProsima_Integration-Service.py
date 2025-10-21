from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Software Architecture Diagram')

# Define nodes for JSON Library components
dot.node('A', 'basic_json', shape='rectangle', color='lightblue')
dot.node('B', 'input_adapter_protocol', shape='rectangle', color='lightblue')
dot.node('C', 'output_adapter_protocol', shape='rectangle', color='lightblue')
dot.node('D', 'lexer', shape='rectangle', color='lightblue')
dot.node('E', 'parser', shape='rectangle', color='lightblue')
dot.node('F', 'json_sax', shape='rectangle', color='lightblue')

# Define nodes for Integration Service components
dot.node('G', 'Core Library', shape='rectangle', color='lightgreen')
dot.node('H', 'System Handles', shape='rectangle', color='lightgreen')
dot.node('I', 'Configuration Parser', shape='rectangle', color='lightgreen')

# Define edges for JSON Library connections
dot.edge('B', 'A', 'reads', arrowhead='vee', color='blue')
dot.edge('C', 'A', 'writes', arrowhead='vee', color='blue')
dot.edge('D', 'E', 'lexical analysis', arrowhead='vee', color='blue')
dot.edge('E', 'A', 'parses', arrowhead='vee', color='blue')
dot.edge('F', 'A', 'SAX parsing', arrowhead='vee', color='blue')

# Define edges for Integration Service connections
dot.edge('H', 'G', 'adapts', arrowhead='vee', color='green')
dot.edge('I', 'G', 'parses', arrowhead='vee', color='green')

# Define interrelation edge
dot.edge('F', 'H', 'data conversion', arrowhead='vee', color='purple')

# Render the graph
dot.render('architecture_diagram', format='png', cleanup=True)
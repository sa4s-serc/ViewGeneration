from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Pollard\'s Kangaroo ECDLP Solver Architecture')

# Define nodes for key components
dot.node('main', 'main.cpp', shape='rectangle')
dot.node('Kangaroo', 'Kangaroo Class', shape='rectangle')
dot.node('Secp256K1', 'Secp256K1 Class', shape='rectangle')
dot.node('GPUEngine', 'GPU/GPUEngine Class', shape='rectangle')
dot.node('HashTable', 'HashTable Class', shape='rectangle')
dot.node('IntArithmetic', 'Integer Arithmetic Classes', shape='rectangle')
dot.node('Network', 'Network Component', shape='rectangle')
dot.node('Backup', 'Backup Component', shape='rectangle')
dot.node('Thread', 'Thread Management', shape='rectangle')
dot.node('Timer', 'Timer Class', shape='rectangle')

# Define edges for key interactions
dot.edge('main', 'Kangaroo', label='orchestrates', dir='forward')
dot.edge('Kangaroo', 'Secp256K1', label='uses', dir='forward')
dot.edge('Kangaroo', 'GPUEngine', label='uses', dir='forward')
dot.edge('Kangaroo', 'HashTable', label='uses', dir='forward')
dot.edge('Kangaroo', 'Network', label='communicates', dir='bidirectional')
dot.edge('Kangaroo', 'Backup', label='manages', dir='forward')
dot.edge('Kangaroo', 'Thread', label='manages', dir='forward')
dot.edge('Kangaroo', 'Timer', label='measures', dir='forward')
dot.edge('Secp256K1', 'IntArithmetic', label='performs', dir='forward')

# Define styles for visual representation
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', style='solid', color='black')

# Render the graph
dot.render('pollards_kangaroo_architecture', format='png', cleanup=True)
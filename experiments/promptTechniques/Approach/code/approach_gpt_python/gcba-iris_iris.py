from graphviz import Digraph

dot = Digraph(comment='Iris Framework Architecture')

# Nodes
dot.node('D', 'Dispatcher', shape='rectangle')
dot.node('Dock', 'Dock', shape='rectangle')
dot.node('H', 'Handler', shape='rectangle')
dot.node('Hook', 'Hook', shape='rectangle')
dot.node('Flow', 'Flow', shape='ellipse')
dot.node('TP', 'Thread Pool', shape='rectangle')
dot.node('CLI', 'CLI', shape='parallelogram')
dot.node('Logger', 'Logger', shape='rectangle')
dot.node('Validator', 'Validator', shape='rectangle')

# Edges
dot.edge('Dock', 'D', label='sends messages')
dot.edge('D', 'H', label='routes data')
dot.edge('H', 'D', label='responses', dir='back')
dot.edge('Hook', 'D', label='executes logic')
dot.edge('D', 'Hook', label='passes data', dir='back')
dot.edge('D', 'Flow', label='manages flows')
dot.edge('Flow', 'TP', label='executes jobs')
dot.edge('CLI', 'D', label='initializes/executes flows')
dot.edge('Logger', 'D', label='logs events')
dot.edge('Validator', 'D', label='validates config')

# Attributes
dot.attr(label='Iris Framework Architecture')
dot.attr(fontsize='20', color='lightgrey')

# Output
dot.render('iris_framework_architecture', format='png', cleanup=True)
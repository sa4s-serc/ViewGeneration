from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Hexagonal Architecture for Todo Management Project')

# Core Business Logic
dot.node('BusinessLogic', 'Business Logic', shape='rectangle')

# Adapters
dot.node('AdapterTodo', 'Todo Adapter', shape='rectangle')
dot.node('AdapterFactory', 'Todo Adapter Factory', shape='rectangle')

# Ports
dot.node('PortDynamoDB', 'DynamoDB Port', shape='rectangle')
dot.node('PortSQS', 'SQS Port', shape='rectangle')
dot.node('PortLambda', 'Lambda Port', shape='rectangle')
dot.node('PortHTTP', 'HTTP Port', shape='rectangle')
dot.node('PortLogger', 'Logger Port', shape='rectangle')

# External Systems
dot.node('DynamoDB', 'DynamoDB', shape='ellipse')
dot.node('SQS', 'SQS', shape='ellipse')
dot.node('Lambda', 'Lambda', shape='ellipse')
dot.node('HTTP', 'HTTP Server', shape='ellipse')
dot.node('Logger', 'Logger', shape='ellipse')

# Connectors between Business Logic and Adapters
dot.edge('BusinessLogic', 'AdapterTodo', label='use')
dot.edge('BusinessLogic', 'AdapterFactory', label='use')

# Connectors between Adapters and Ports
dot.edge('AdapterTodo', 'PortDynamoDB', label='use')
dot.edge('AdapterFactory', 'PortDynamoDB', label='create')
dot.edge('AdapterFactory', 'PortSQS', label='create')
dot.edge('AdapterFactory', 'PortLambda', label='create')
dot.edge('AdapterFactory', 'PortHTTP', label='create')
dot.edge('AdapterFactory', 'PortLogger', label='create')

# Connectors between Ports and External Systems
dot.edge('PortDynamoDB', 'DynamoDB', label='connect')
dot.edge('PortSQS', 'SQS', label='connect')
dot.edge('PortLambda', 'Lambda', label='connect')
dot.edge('PortHTTP', 'HTTP', label='connect')
dot.edge('PortLogger', 'Logger', label='connect')

# Render the graph to a file
dot.render('hexagonal_architecture', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Noob Platform Architecture', format='png')

# Add nodes for each microservice
dot.node('Auth', 'Auth\n(Manages user authentication and authorization)', shape='rect', style='filled', fillcolor='lightblue')
dot.node('Frontend', 'Frontend\n(Provides user interface)', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('Problems', 'Problems\n(Manages problem definitions)', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('Submissions', 'Submissions\n(Handles user submissions)', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('Executor', 'Executor\n(Executes code submissions)', shape='rect', style='filled', fillcolor='lightgrey')

# Add nodes for infrastructure components
dot.node('RabbitMQ', 'RabbitMQ\n(Message Queue)', shape='ellipse', style='filled', fillcolor='lightpink')
dot.node('MongoDB', 'MongoDB\n(Database)', shape='cylinder', style='filled', fillcolor='lightgoldenrod')
dot.node('Redis', 'Redis\n(Session Store)', shape='cylinder', style='filled', fillcolor='lightsteelblue')
dot.node('Jaeger', 'Jaeger\n(Distributed Tracing)', shape='ellipse', style='filled', fillcolor='lightcyan')

# Add edges for communication between services
dot.edge('Frontend', 'Auth', 'HTTP')
dot.edge('Frontend', 'Problems', 'HTTP')
dot.edge('Frontend', 'Submissions', 'WebSocket')
dot.edge('Submissions', 'RabbitMQ', 'Publishes')
dot.edge('Executor', 'RabbitMQ', 'Consumes')
dot.edge('Executor', 'Submissions', 'Publishes Results')
dot.edge('Auth', 'MongoDB', 'Reads/Writes')
dot.edge('Problems', 'MongoDB', 'Reads/Writes')
dot.edge('Submissions', 'MongoDB', 'Reads/Writes')
dot.edge('Auth', 'Redis', 'Reads/Writes')
dot.edge('Submissions', 'Redis', 'Reads/Writes')
dot.edge('Submissions', 'Jaeger', 'Traces')
dot.edge('Executor', 'Jaeger', 'Traces')

# Add API Gateway node and edges
dot.node('API Gateway', 'API Gateway\n(Routes requests)', shape='rect', style='dashed')
dot.edge('API Gateway', 'Frontend', 'Routes')

# Render the graph to a file
dot.render('noob_platform_architecture')
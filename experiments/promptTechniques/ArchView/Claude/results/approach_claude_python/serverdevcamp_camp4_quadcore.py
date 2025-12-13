from graphviz import Digraph

dot = Digraph('Microservices Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('client', 'Frontend\n(React)')
dot.node('gateway', 'API Gateway\n(Spring Cloud Gateway)')
dot.node('auth', 'Auth Server\n(Spring Boot)')
dot.node('activity', 'User Activity\n(Spring Boot)')
dot.node('pipeline', 'Data Pipeline\n(Kafka)')
dot.node('process', 'Data Processing\n(Spark)')
dot.node('send', 'Data Sending\n(Spring Boot)')

# Add databases
dot.attr('node', shape='cylinder')
dot.node('cassandra', 'Cassandra')
dot.node('redis', 'Redis')

# Add message broker
dot.attr('node', shape='hexagon')
dot.node('kafka', 'Kafka')

# Define edges
dot.edge('client', 'gateway')
dot.edge('gateway', 'auth', 'JWT auth')
dot.edge('gateway', 'activity', 'User actions')
dot.edge('gateway', 'send', 'Data requests')
dot.edge('auth', 'redis', 'Store tokens')
dot.edge('pipeline', 'kafka', 'Stream data')
dot.edge('kafka', 'process', 'Process data')
dot.edge('process', 'cassandra', 'Store results')
dot.edge('send', 'cassandra', 'Query data')
dot.edge('activity', 'cassandra', 'Store activity')

# Save the diagram
dot.render('architecture_diagram', format='png', cleanup=True)
import graphviz

dot = graphviz.Digraph(comment='Doping Control System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('frontend', 'Frontend\n(React/MUI)')
dot.node('auth', 'Authentication\nService')
dot.node('athlete', 'Athlete\nAvailability\nService')
dot.node('test', 'Test Scheduling\n& Reporting\nService')
dot.node('dynamo', 'DynamoDB', shape='cylinder')

# Add connections
dot.edge('frontend', 'auth', 'JWT Auth')
dot.edge('frontend', 'athlete', 'REST API')
dot.edge('frontend', 'test', 'REST API')
dot.edge('auth', 'dynamo', 'User Data')
dot.edge('athlete', 'dynamo', 'Availability\nData')
dot.edge('test', 'dynamo', 'Test Results')

# Add cluster for backend services
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Backend Microservices', style='dashed')
    c.node('auth')
    c.node('athlete')
    c.node('test')

# Save the diagram
dot.render('doping_control_architecture', format='png', cleanup=True)
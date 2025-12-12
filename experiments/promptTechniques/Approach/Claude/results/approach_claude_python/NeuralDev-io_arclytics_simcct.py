from graphviz import Digraph

dot = Digraph(comment='Arclytics SimCCT Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('client', 'Client\n(React + Redux)')
dot.node('simcct', 'SimCCT Service\n(Flask)')
dot.node('user_mgmt', 'User Management\n(Flask Blueprint)')
dot.node('analytics', 'Analytics Service')
dot.node('mongodb', 'MongoDB')
dot.node('redis', 'Redis')
dot.node('celery', 'Celery')
dot.node('logging', 'Logging\n(Fluentd)')
dot.node('elastic', 'Elasticsearch')
dot.node('kibana', 'Kibana')

# Create subgraph for data persistence
with dot.subgraph(name='cluster_data') as c:
    c.attr(label='Data Layer')
    c.node('mongodb')
    c.node('redis')

# Create subgraph for monitoring
with dot.subgraph(name='cluster_monitoring') as c:
    c.attr(label='Monitoring')
    c.node('logging')
    c.node('elastic')
    c.node('kibana')

# Add edges
dot.edge('client', 'simcct', 'REST API')
dot.edge('simcct', 'user_mgmt', 'Authentication')
dot.edge('simcct', 'mongodb', 'Data Access')
dot.edge('simcct', 'redis', 'Session/Cache')
dot.edge('simcct', 'celery', 'Async Tasks')
dot.edge('simcct', 'analytics', 'Usage Metrics')
dot.edge('simcct', 'logging', 'Log Events')
dot.edge('logging', 'elastic')
dot.edge('elastic', 'kibana', 'Visualization')
dot.edge('celery', 'redis', 'Message Queue')

# Set graph attributes
dot.attr(fontsize='20')
dot.attr(label='Arclytics SimCCT - Microservices Architecture')

# Render the diagram
dot.render('arclytics_architecture', view=True, format='png')
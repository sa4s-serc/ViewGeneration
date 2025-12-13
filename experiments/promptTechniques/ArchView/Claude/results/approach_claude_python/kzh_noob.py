import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='noob Code Execution Platform Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Add services
dot.node('frontend', 'Frontend\n(Gin Web Framework)')
dot.node('auth', 'Auth Service')
dot.node('problems', 'Problems Service')
dot.node('submissions', 'Submissions Service')
dot.node('executor', 'Executor Service\n(Docker-in-Docker)')

# Add databases and message queue
dot.attr('node', shape='cylinder')
dot.node('mongodb', 'MongoDB')
dot.node('redis', 'Redis\n(Sessions)')
dot.node('rabbitmq', 'RabbitMQ')

# Add monitoring
dot.attr('node', shape='hexagon')
dot.node('jaeger', 'Jaeger\n(Tracing)')

# Add edges
dot.edge('frontend', 'auth', 'authenticate')
dot.edge('frontend', 'problems', 'fetch problems')
dot.edge('frontend', 'submissions', 'submit code')
dot.edge('submissions', 'rabbitmq', 'publish')
dot.edge('executor', 'rabbitmq', 'consume')
dot.edge('executor', 'submissions', 'results')

# Database connections
dot.edge('auth', 'mongodb')
dot.edge('problems', 'mongodb')
dot.edge('submissions', 'mongodb')
dot.edge('auth', 'redis')

# Monitoring connections
dot.edge('frontend', 'jaeger')
dot.edge('auth', 'jaeger')
dot.edge('problems', 'jaeger')
dot.edge('submissions', 'jaeger')
dot.edge('executor', 'jaeger')

# Add subgraph for infrastructure
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Kubernetes Cluster')
    c.node('ingress', 'Ingress')
    c.edge('ingress', 'frontend')

# Set graph attributes
dot.attr(label='noob Code Execution Platform Architecture\nKubernetes-based Microservices')
dot.attr(fontsize='20')

# Save the diagram
dot.render('architecture_diagram', format='png', cleanup=True)
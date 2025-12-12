from graphviz import Digraph

dot = Digraph(comment='Software Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightblue')

# Add components
dot.node('frontend', 'Frontend\n(React/Redux)')
dot.node('api', 'API Gateway\n(Spring Boot)')
dot.node('auth', 'Authentication\n(Spring Security)')
dot.node('services', 'Microservices')
dot.node('db', 'Databases\n(MySQL/MongoDB)')
dot.node('queue', 'Message Queue\n(ZeroMQ)')
dot.node('ci_cd', 'CI/CD Pipeline\n(Azure DevOps)')
dot.node('monitor', 'Monitoring\n(New Relic)')
dot.node('logging', 'Logging\n(Elastic Stack)')

# Add edges
dot.edge('frontend', 'api')
dot.edge('api', 'auth')
dot.edge('api', 'services')
dot.edge('services', 'db')
dot.edge('services', 'queue')
dot.edge('ci_cd', 'frontend')
dot.edge('ci_cd', 'api')
dot.edge('ci_cd', 'services')
dot.edge('monitor', 'api')
dot.edge('monitor', 'services')
dot.edge('monitor', 'db')
dot.edge('logging', 'api')
dot.edge('logging', 'services')
dot.edge('logging', 'db')

# Save the diagram
dot.render('architecture_view', format='png', cleanup=True)
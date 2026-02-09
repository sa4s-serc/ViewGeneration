from graphviz import Digraph

dot = Digraph(comment='Audit Framework Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add components
dot.node('client_lib', 'Client Library\n(Spring Boot Starter)')
dot.node('app_server', 'Application Server\n(/app)')
dot.node('core', 'Core Module\n(/core)')
dot.node('kafka', 'Kafka\nEvent Streaming')
dot.node('elastic', 'Elasticsearch\nStorage')
dot.node('specs', 'OpenAPI Specs\n(/specs)')

# Add subcomponents
with dot.subgraph(name='cluster_app') as app:
    app.attr(label='Application Server Components')
    app.node('consumer', 'ConsumerService.kt')
    app.node('repo', 'AuditEventRepositoryService.kt')
    app.node('main', 'Application.kt')

# Add connections
dot.edge('client_lib', 'kafka', 'Audit Events')
dot.edge('kafka', 'consumer', 'Consume Events')
dot.edge('consumer', 'repo', 'Store Events')
dot.edge('repo', 'elastic', 'Persist Data')
dot.edge('core', 'client_lib', 'Use')
dot.edge('core', 'app_server', 'Use')
dot.edge('specs', 'core', 'Generate Code')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('audit_framework_architecture', view=True, format='png')
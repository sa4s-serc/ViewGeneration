from graphviz import Digraph

dot = Digraph(comment='Activiti 7 Cloud Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('core', 'Activiti Core\nProcess Engine')
dot.node('runtime', 'Runtime Bundle\nStateless Service')
dot.node('connectors', 'Cloud Connectors')
dot.node('query', 'Query Service')
dot.node('audit', 'Audit Service')
dot.node('notification', 'Notification Service')
dot.node('gateway', 'API Gateway')
dot.node('keycloak', 'Keycloak\nIdentity Management')
dot.node('stream', 'Spring Cloud Stream')
dot.node('modeling', 'BPMN Modeling\nApplication')
dot.node('helm', 'Helm Charts')
dot.node('jenkins', 'Jenkins X\nCI/CD')

# Add relationships
dot.edge('gateway', 'runtime')
dot.edge('gateway', 'query')
dot.edge('gateway', 'audit')
dot.edge('gateway', 'notification')
dot.edge('runtime', 'core')
dot.edge('runtime', 'connectors')
dot.edge('runtime', 'stream')
dot.edge('query', 'stream')
dot.edge('audit', 'stream')
dot.edge('notification', 'stream')
dot.edge('keycloak', 'gateway')
dot.edge('modeling', 'runtime')
dot.edge('helm', 'runtime')
dot.edge('helm', 'query')
dot.edge('helm', 'audit')
dot.edge('helm', 'notification')
dot.edge('jenkins', 'helm')

# Print the dot source
print(dot.source)

# Render the diagram
dot.render('activiti_architecture', view=True, format='png')
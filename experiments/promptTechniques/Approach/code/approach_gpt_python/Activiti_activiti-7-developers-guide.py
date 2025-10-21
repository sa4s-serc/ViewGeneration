from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Activiti 7 Cloud Architecture', format='png')

# Define node styles
node_style = {'style': 'filled', 'shape': 'rectangle', 'color': 'lightblue'}
connector_style = {'style': 'filled', 'shape': 'rectangle', 'color': 'lightgreen'}
service_style = {'style': 'filled', 'shape': 'rectangle', 'color': 'lightyellow'}
gateway_style = {'style': 'filled', 'shape': 'rectangle', 'color': 'lightcoral'}

# Add nodes
dot.node('Core', 'Activiti Core', **node_style)
dot.node('Runtime', 'Activiti Cloud Runtime Bundle', **node_style)
dot.node('Connectors', 'Activiti Cloud Connectors', **connector_style)
dot.node('Query', 'Activiti Cloud Query Service', **service_style)
dot.node('Audit', 'Activiti Cloud Audit Service', **service_style)
dot.node('Notification', 'Activiti Cloud Notification Service', **service_style)
dot.node('Gateway', 'Gateway', **gateway_style)
dot.node('SSO', 'Identity Management / SSO', **node_style)
dot.node('SpringCloud', 'Spring Cloud Integration', **node_style)
dot.node('Modeling', 'BPMN Modeling Application', **node_style)
dot.node('Helm', 'Helm Charts', **node_style)
dot.node('JenkinsX', 'Jenkins X', **node_style)

# Add edges
dot.edge('Core', 'Runtime', label='Executes BPMN Processes')
dot.edge('Runtime', 'Connectors', label='Integrates with External Services')
dot.edge('Runtime', 'Query', label='Aggregates Data')
dot.edge('Runtime', 'Audit', label='Sends Events')
dot.edge('Runtime', 'Notification', label='Real-time Updates')
dot.edge('Gateway', 'Runtime', label='Single Entry Point')
dot.edge('SSO', 'Gateway', label='Authentication & Authorization')
dot.edge('SpringCloud', 'Runtime', label='Asynchronous Communication')
dot.edge('Modeling', 'Runtime', label='Design BPMN Definitions')
dot.edge('Helm', 'Runtime', label='Deployment to Kubernetes')
dot.edge('JenkinsX', 'Helm', label='CI/CD Automation')

# Render the graph to a file
dot.render('activiti7_cloud_architecture')
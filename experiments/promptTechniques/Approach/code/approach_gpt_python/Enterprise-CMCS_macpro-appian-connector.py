from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Enterprise-CMCS_macpro-appian-connector Architecture')

# Add nodes for each core component
dot.node('Appian', 'Appian', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Kafka Connector', 'Kafka Connector', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('BigMAC', 'BigMAC', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('ECS', 'ECS', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('SNS', 'SNS', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('CloudWatch', 'CloudWatch', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('IAM', 'IAM', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('GitHub Actions', 'GitHub Actions', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('SSM Parameter Store', 'SSM Parameter Store', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('Secrets Manager', 'Secrets Manager', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('Jira', 'Jira', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('DORA Dashboard', 'DORA Dashboard', shape='rectangle', style='filled', fillcolor='lightyellow')

# Add edges to represent communication and control flow
dot.edge('Appian', 'Kafka Connector', label='Data Changes')
dot.edge('Kafka Connector', 'BigMAC', label='Stream Data')
dot.edge('Kafka Connector', 'ECS', label='Deploy')
dot.edge('Kafka Connector', 'SNS', label='Alerting')
dot.edge('Kafka Connector', 'CloudWatch', label='Monitoring')
dot.edge('Kafka Connector', 'IAM', label='Security')
dot.edge('GitHub Actions', 'Kafka Connector', label='CI/CD')
dot.edge('SSM Parameter Store', 'Kafka Connector', label='Configuration')
dot.edge('Secrets Manager', 'Kafka Connector', label='Secrets Management')
dot.edge('SNS', 'Jira', label='Sync Issues')
dot.edge('CloudWatch', 'DORA Dashboard', label='Track Metrics')

# Render the graph to a file
dot.render('enterprise_cmcs_macpro_appian_connector_architecture', format='png', cleanup=True)
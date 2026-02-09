from graphviz import Digraph

dot = Digraph(comment='Enterprise-CMCS_macpro-appian-connector Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('kafka', 'Kafka Connector')
dot.node('appian', 'Appian')
dot.node('bigmac', 'BigMAC')
dot.node('ecs', 'ECS Service')
dot.node('sns', 'SNS Topic')
dot.node('cloudwatch', 'CloudWatch')
dot.node('iam', 'IAM')
dot.node('ssm', 'SSM Parameter Store')
dot.node('secrets', 'Secrets Manager')

# Add subgraph for monitoring and alerting
with dot.subgraph(name='cluster_monitoring') as monitoring:
    monitoring.attr(label='Monitoring & Alerting')
    monitoring.node('alerts', 'Alerts Service')
    monitoring.node('dashboard', 'Dashboard')

# Add edges
dot.edge('appian', 'kafka', 'Data Changes')
dot.edge('kafka', 'ecs', 'Stream')
dot.edge('ecs', 'bigmac', 'Data Transfer')
dot.edge('ecs', 'sns', 'Notifications')
dot.edge('sns', 'alerts', 'Trigger')
dot.edge('cloudwatch', 'alerts', 'Metrics')
dot.edge('ssm', 'ecs', 'Config')
dot.edge('secrets', 'ecs', 'Credentials')
dot.edge('iam', 'ecs', 'Permissions')
dot.edge('alerts', 'dashboard', 'Status')

# Print the dot source
print(dot.source)

# Render the diagram
dot.render('architecture', format='png', cleanup=True)
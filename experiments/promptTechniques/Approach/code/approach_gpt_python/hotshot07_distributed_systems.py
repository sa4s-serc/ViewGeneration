from graphviz import Digraph

dot = Digraph(comment='Doping Control System Architecture')
dot.attr(rankdir='LR')

# Frontend
dot.node('Frontend', 'React Frontend', shape='box', style='filled', fillcolor='lightblue')

# Backend Services
dot.node('AuthService', 'Authentication Service', shape='box', style='filled', fillcolor='lightcoral')
dot.node('AccountService', 'Account Management Service', shape='box', style='filled', fillcolor='lightcoral')
dot.node('TrackingService', 'Athlete Tracking Service', shape='box', style='filled', fillcolor='lightcoral')
dot.node('ScheduleService', 'Test Scheduling Service', shape='box', style='filled', fillcolor='lightcoral')

# Data Storage
dot.node('DynamoDB', 'DynamoDB', shape='cylinder', style='filled', fillcolor='lightgrey')

# Deployment
dot.node('Kubernetes', 'Kubernetes Cluster', shape='box3d', style='dotted')

# Connections
dot.edge('Frontend', 'AuthService', label='REST API', dir='both')
dot.edge('Frontend', 'AccountService', label='REST API', dir='both')
dot.edge('Frontend', 'TrackingService', label='REST API', dir='both')
dot.edge('Frontend', 'ScheduleService', label='REST API', dir='both')

dot.edge('AuthService', 'DynamoDB', label='Data Storage', dir='both')
dot.edge('AccountService', 'DynamoDB', label='Data Storage', dir='both')
dot.edge('TrackingService', 'DynamoDB', label='Data Storage', dir='both')
dot.edge('ScheduleService', 'DynamoDB', label='Data Storage', dir='both')

# Kubernetes Deployment
dot.edge('AuthService', 'Kubernetes', label='Deployed on', dir='none')
dot.edge('AccountService', 'Kubernetes', label='Deployed on', dir='none')
dot.edge('TrackingService', 'Kubernetes', label='Deployed on', dir='none')
dot.edge('ScheduleService', 'Kubernetes', label='Deployed on', dir='none')

# Legend
with dot.subgraph(name='cluster_legend') as legend:
    legend.attr(label='Legend', style='dashed')
    legend.node('REST API', 'REST API', shape='point')
    legend.node('Data Storage', 'Data Storage', shape='point')
    legend.node('Deployed on', 'Deployed on', shape='point')

# Display the graph
dot.render('doping_control_system_architecture', format='png', cleanup=True)

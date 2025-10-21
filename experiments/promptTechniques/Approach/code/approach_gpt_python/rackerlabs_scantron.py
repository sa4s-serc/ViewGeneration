from graphviz import Digraph

dot = Digraph(comment='Scantron Architecture', format='png')
dot.attr(rankdir='LR', size='8,5')

# Define styles for different types of nodes
styles = {
    'console': {'shape': 'rectangle', 'style': 'filled', 'color': 'lightblue'},
    'engine': {'shape': 'rectangle', 'style': 'filled', 'color': 'lightgreen'},
    'rest_api': {'shape': 'ellipse', 'style': 'filled', 'color': 'lightcoral'},
    'storage': {'shape': 'cylinder', 'style': 'filled', 'color': 'lightgrey'},
    'email': {'shape': 'octagon', 'style': 'filled', 'color': 'lightyellow'},
    'ansible': {'shape': 'parallelogram', 'style': 'filled', 'color': 'lightpink'},
    'queue': {'shape': 'diamond', 'style': 'filled', 'color': 'lightgoldenrod1'},
}

# Nodes
dot.node('Console', 'Console (Web Front-End)', **styles['console'])
dot.node('API', 'REST API', **styles['rest_api'])
dot.node('Engines', 'Engines (Scanning Nodes)', **styles['engine'])
dot.node('NFS', 'Shared NFS Volume', **styles['storage'])
dot.node('Email', 'Email Alerts', **styles['email'])
dot.node('Ansible', 'Ansible Playbooks', **styles['ansible'])
dot.node('Queue', 'Redis Queue', **styles['queue'])

# Edges
dot.edge('Console', 'API', label='Communicates through', arrowhead='vee')
dot.edge('Engines', 'API', label='Polls for tasks', arrowhead='vee')
dot.edge('Engines', 'NFS', label='Stores results', arrowhead='vee')
dot.edge('NFS', 'Console', label='Processes results', arrowhead='vee')
dot.edge('Console', 'Email', label='Sends alerts', arrowhead='vee')
dot.edge('Ansible', 'Console', label='Deploys', arrowhead='vee')
dot.edge('Ansible', 'Engines', label='Deploys', arrowhead='vee')
dot.edge('Console', 'Queue', label='Queues tasks', arrowhead='vee')

# Render the diagram
dot.render('scantron_architecture', view=True)
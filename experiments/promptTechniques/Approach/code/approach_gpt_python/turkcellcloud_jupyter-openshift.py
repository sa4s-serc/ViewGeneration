from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='JupyterHub on OpenShift Architecture')

# Define nodes
dot.node('JH', 'JupyterHub', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('JL', 'JupyterLab', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('KS', 'KubeSpawner', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('PG', 'PostgreSQL', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('AD', 'Active Directory/LDAP', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('PV', 'Persistent Volumes', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('NP', 'Network Policies', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('CI', 'Custom Images', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('IS', 'Idle Server Culling', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('OT', 'OpenShift Templates', shape='rectangle', style='filled', fillcolor='lightgrey')

# Define edges
dot.edge('AD', 'JH', 'LDAP Authentication', dir='both')
dot.edge('JH', 'JL', 'Provides UI', dir='both')
dot.edge('JH', 'KS', 'Manages Pods', dir='both')
dot.edge('KS', 'PG', 'Stores Config', dir='both')
dot.edge('JH', 'PV', 'Uses Persistent Storage', dir='both')
dot.edge('JH', 'NP', 'Applies Security Policies', dir='both')
dot.edge('JH', 'CI', 'Builds Custom Images', dir='both')
dot.edge('JH', 'IS', 'Culls Idle Servers', dir='both')
dot.edge('JH', 'OT', 'Uses Templates for Deployment', dir='both')

# Render the graph to a file
dot.render('jupyterhub_openshift_architecture', format='png', cleanup=True)
import graphviz

dot = graphviz.Digraph(comment='JupyterHub on OpenShift Architecture')
dot.attr(rankdir='TB', size='8,8')

# Define nodes
dot.node('client', 'Client', shape='ellipse')
dot.node('router', 'OpenShift Router', shape='box')
dot.node('jupyterhub', 'JupyterHub', shape='box')
dot.node('kubespawner', 'KubeSpawner', shape='box')
dot.node('notebook', 'Notebook Server', shape='box')
dot.node('ldap', 'LDAP/AD', shape='cylinder')
dot.node('postgresql', 'PostgreSQL', shape='cylinder')
dot.node('storage', 'Persistent Storage', shape='cylinder')
dot.node('network_policy', 'Network Policy', shape='note')

# Define edges
dot.edge('client', 'router', label='HTTP/HTTPS')
dot.edge('router', 'jupyterhub', label='HTTP/HTTPS')
dot.edge('jupyterhub', 'ldap', label='LDAP Auth', style='dashed')
dot.edge('jupyterhub', 'postgresql', label='Database', style='dashed')
dot.edge('jupyterhub', 'kubespawner', label='Spawner API')
dot.edge('kubespawner', 'notebook', label='Pod Creation')
dot.edge('notebook', 'storage', label='Persistent Data')
dot.edge('network_policy', 'notebook', label='Restricts Traffic', style='dotted')

# Add cluster boundary
with dot.subgraph(name='cluster_openshift') as c:
    c.attr(label='OpenShift Cluster', style='dashed')
    c.node('jupyterhub')
    c.node('kubespawner')
    c.node('notebook')
    c.node('postgresql')
    c.node('storage')
    c.node('network_policy')

dot.render('jupyterhub_architecture', format='png', cleanup=True)
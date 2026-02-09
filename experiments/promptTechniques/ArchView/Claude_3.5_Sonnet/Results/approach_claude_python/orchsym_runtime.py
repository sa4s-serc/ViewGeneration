import graphviz

# Create a new directed graph
g = graphviz.Digraph('NiFi_Architecture', filename='nifi_architecture.gv')
g.attr(rankdir='TB')

# Add clusters/subgraphs
with g.subgraph(name='cluster_core') as core:
    core.attr(label='Core Framework', style='rounded', color='blue')
    core.node('flow_controller', 'Flow Controller\n(Central Management)', shape='box')
    core.node('proc_scheduler', 'Process Scheduler', shape='box')
    core.node('flow_sync', 'Flow Synchronizer', shape='box')
    core.node('state_mgr', 'State Manager', shape='box')

with g.subgraph(name='cluster_repos') as repos:
    repos.attr(label='Repositories', style='rounded', color='green')
    repos.node('flowfile_repo', 'FlowFile Repository', shape='cylinder')
    repos.node('content_repo', 'Content Repository', shape='cylinder')
    repos.node('prov_repo', 'Provenance Repository', shape='cylinder')

with g.subgraph(name='cluster_security') as security:
    security.attr(label='Security Layer', style='rounded', color='red')
    security.node('auth', 'Authentication & \nAuthorization', shape='box')
    security.node('ssl', 'SSL Context Service', shape='box')
    security.node('key_mgmt', 'Key Management', shape='box')

with g.subgraph(name='cluster_processing') as processing:
    processing.attr(label='Data Processing', style='rounded', color='purple')
    processing.node('proc_session', 'Process Session\n(Transactional Context)', shape='box')
    processing.node('flow_file', 'FlowFile\n(Data + Attributes)', shape='box')
    processing.node('proc_group', 'Process Group', shape='box')
    processing.node('controller_svc', 'Controller Services', shape='box')

# Add edges
# Core connections
g.edge('flow_controller', 'proc_scheduler')
g.edge('flow_controller', 'flow_sync')
g.edge('flow_controller', 'state_mgr')
g.edge('flow_controller', 'controller_svc')

# Processing connections
g.edge('proc_scheduler', 'proc_session')
g.edge('proc_session', 'flow_file')
g.edge('flow_file', 'content_repo')
g.edge('proc_session', 'flowfile_repo')
g.edge('proc_session', 'prov_repo')
g.edge('proc_group', 'flow_controller')

# Security connections
g.edge('auth', 'flow_controller')
g.edge('ssl', 'flow_controller')
g.edge('key_mgmt', 'flow_controller')

# Set graph attributes
g.attr(fontname='Arial')
g.attr('node', fontname='Arial')
g.attr('edge', fontname='Arial')

# Render the graph
g.render('nifi_architecture', format='png', cleanup=True)
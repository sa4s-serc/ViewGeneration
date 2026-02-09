import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='MLAB Architecture')
dot.attr(rankdir='TB')
dot.attr(fontname='Helvetica')
dot.attr(bgcolor='white')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightgrey', fontname='Helvetica')

# Dashboard Components Cluster
with dot.subgraph(name='cluster_dashboard') as d:
    d.attr(label='Dashboard Component', style='rounded', color='blue', fontcolor='blue')
    
    # Core components
    d.node('flask_core', 'Dashboard Core\nFlask + Security')
    d.node('dal', 'Data Access Layer\nRepositories')
    d.node('interactors', 'Interactors\nUse Cases')
    d.node('monitor', 'Real-time\nMonitoring')
    d.node('api', 'API Endpoints')
    d.node('frontend', 'Frontend\nAdminLTE')
    d.node('publisher', 'Model Publisher')

# Worker Service Cluster
with dot.subgraph(name='cluster_worker') as w:
    w.attr(label='Worker Service', style='rounded', color='darkgreen', fontcolor='darkgreen')
    
    w.node('model_mgmt', 'Model Management')
    w.node('zk_int', 'ZooKeeper\nIntegration')
    w.node('error_handle', 'Error Handling')
    w.node('http_api', 'HTTP API')

# External Services Cluster
with dot.subgraph(name='cluster_external') as e:
    e.attr(label='External Services', style='rounded', color='red', fontcolor='red')
    
    e.node('zookeeper', 'ZooKeeper', shape='cylinder')
    e.node('mongodb', 'MongoDB', shape='cylinder')
    e.node('docker', 'Docker', shape='rectangle')

# Dashboard internal connections
dot.edge('flask_core', 'dal')
dot.edge('flask_core', 'interactors')
dot.edge('flask_core', 'api')
dot.edge('frontend', 'api')
dot.edge('interactors', 'publisher')
dot.edge('monitor', 'flask_core')

# Worker internal connections
dot.edge('model_mgmt', 'zk_int')
dot.edge('model_mgmt', 'error_handle')
dot.edge('model_mgmt', 'http_api')

# Cross-component connections
dot.edge('dal', 'mongodb')
dot.edge('dal', 'zookeeper')
dot.edge('zk_int', 'zookeeper')
dot.edge('publisher', 'zookeeper')
dot.edge('docker', 'flask_core')
dot.edge('docker', 'model_mgmt')

# Save the diagram
dot.render('mlab_architecture', format='png', cleanup=True)
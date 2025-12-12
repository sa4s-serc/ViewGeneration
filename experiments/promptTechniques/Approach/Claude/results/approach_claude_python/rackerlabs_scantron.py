from graphviz import Digraph

dot = Digraph(comment='Scantron Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('console', 'Console\n(Web Front-end)')
dot.node('api', 'REST API\n(Django REST Framework)')
dot.node('scheduler', 'Scan Scheduler\n(django-recurrence)')
dot.node('queue', 'Redis Queue')
dot.node('db', 'Database')
dot.node('nfs', 'NFS Storage')

# Add engine nodes
with dot.subgraph(name='cluster_engines') as c:
    c.attr(label='Scanning Engines')
    c.node('engine1', 'Engine 1')
    c.node('engine2', 'Engine 2')
    c.node('engine3', 'Engine 3')

# Add result processors
dot.node('results', 'Scan Results Processor')
dot.node('analytics', 'Big Data Analytics')

# Define relationships
dot.edge('console', 'api')
dot.edge('api', 'scheduler')
dot.edge('scheduler', 'queue')
dot.edge('queue', 'engine1')
dot.edge('queue', 'engine2')
dot.edge('queue', 'engine3')
dot.edge('engine1', 'nfs')
dot.edge('engine2', 'nfs')
dot.edge('engine3', 'nfs')
dot.edge('nfs', 'results')
dot.edge('results', 'analytics')
dot.edge('api', 'db')
dot.edge('scheduler', 'db')

# Save the diagram
dot.render('scantron_architecture', format='png', cleanup=True)
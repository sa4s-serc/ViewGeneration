import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Software Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('client', 'Client Applications')
dot.node('redis', 'Redis Core')
dot.node('codis', 'Codis Proxy')
dot.node('lua', 'Lua Scripting')
dot.node('sentinel', 'Redis Sentinel')
dot.node('data_structures', 'Data Structures\n(SDS, Hash Tables,\nSkip Lists, etc)')

# Add storage components
dot.node('persistence', 'Persistence Layer\n(RDB + AOF)')
dot.node('jemalloc', 'Memory Management\n(Jemalloc)')

# Add monitoring components
dot.node('monitor', 'Monitoring\n(Latency, Slow Log)')

# Define edges
dot.edge('client', 'codis')
dot.edge('codis', 'redis')
dot.edge('redis', 'data_structures')
dot.edge('redis', 'persistence')
dot.edge('redis', 'jemalloc')
dot.edge('redis', 'lua')
dot.edge('sentinel', 'redis')
dot.edge('redis', 'monitor')

# Create subgraph for core components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components')
    core.node('data_structures')
    core.node('persistence')
    core.node('jemalloc')

print(dot.source)
dot.render('architecture_view', view=True, format='png')
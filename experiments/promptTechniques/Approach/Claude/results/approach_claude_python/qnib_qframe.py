import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='QFrame Architecture View')
dot.attr(rankdir='TB')

# Add node attributes
dot.attr('node', shape='box', style='rounded')

# Define nodes
dot.node('collectors', 'Collectors\n(Data Ingestion)')
dot.node('filters', 'Filters\n(Data Processing)')
dot.node('handlers', 'Handlers\n(Data Output)')
dot.node('qchan', 'QChan\n(Message Broadcasting)')
dot.node('config', 'Configuration\n(YAML/JSON)')
dot.node('plugins', 'Plugin System')
dot.node('types', 'Types\n(Metric/Container)')

# Add subgraph for core components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components')
    core.node('microkernel', 'Microkernel')
    core.node('container_inv', 'Container Inventory')

# Define edges
dot.edge('collectors', 'qchan')
dot.edge('qchan', 'filters')
dot.edge('filters', 'qchan')
dot.edge('qchan', 'handlers')
dot.edge('config', 'microkernel')
dot.edge('plugins', 'microkernel')
dot.edge('microkernel', 'collectors')
dot.edge('microkernel', 'filters')
dot.edge('microkernel', 'handlers')
dot.edge('types', 'collectors')
dot.edge('types', 'filters')
dot.edge('types', 'handlers')
dot.edge('container_inv', 'filters')

# Set graph attributes
dot.attr(label='qnib_qframe Architecture\nMicrokernel-based Plugin Architecture', labelloc='t')
dot.attr(fontsize='16')

# Save the diagram
dot.render('qframe_architecture', format='png', cleanup=True)
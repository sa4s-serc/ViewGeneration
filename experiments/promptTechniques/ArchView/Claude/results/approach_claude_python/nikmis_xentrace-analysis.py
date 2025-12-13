from graphviz import Digraph

dot = Digraph(comment='Xen Performance Analysis Tool Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('xentrace', 'Xentrace\nData Capture')
dot.node('reader', 'Reader\nEvent Parsing & Sorting')
dot.node('event_handler', 'Event Handler\nEvent Distribution')

# Add analysis modules
with dot.subgraph(name='cluster_analysis') as c:
    c.attr(label='Analysis Modules')
    c.node('cpu_time', 'CPU Time\nSharing')
    c.node('cpu_wait', 'CPU Wait\nScheduling')
    c.node('xen_dom', 'Xen Domain\nTime')
    c.node('blk_io', 'Block I/O\nQueues')
    c.node('xen_stats', 'Xen Event\nStats')
    c.node('trap', 'Trap\nCounting')

# Add edges
dot.edge('xentrace', 'reader', 'trace data')
dot.edge('reader', 'event_handler', 'sorted events')
dot.edge('event_handler', 'cpu_time')
dot.edge('event_handler', 'cpu_wait')
dot.edge('event_handler', 'xen_dom')
dot.edge('event_handler', 'blk_io')
dot.edge('event_handler', 'xen_stats')
dot.edge('event_handler', 'trap')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('xen_performance_architecture', format='png', cleanup=True)
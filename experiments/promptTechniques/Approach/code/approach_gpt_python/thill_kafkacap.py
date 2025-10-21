from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='KafkaCap Architectural Overview', format='png')

# Define nodes for key components
dot.node('A', 'AeronCaptureDevice', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('M', 'MulticastCaptureDevice', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('W', 'WebsocketCaptureDevice', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('D', 'Deduplicator', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('DP', 'DedupStrategy', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Q', 'CaptureQueue', shape='rectangle', style='filled', fillcolor='orange')
dot.node('R', 'RecordPopulator', shape='rectangle', style='filled', fillcolor='yellow')
dot.node('RS', 'RecoveryService', shape='rectangle', style='filled', fillcolor='pink')

# Define connections between nodes
dot.edge('A', 'D', label='writes to', style='dotted')
dot.edge('M', 'D', label='writes to', style='dotted')
dot.edge('W', 'D', label='writes to', style='dotted')
dot.edge('D', 'DP', label='uses', style='dotted')
dot.edge('D', 'Q', label='buffers', style='dotted')
dot.edge('Q', 'R', label='creates', style='dotted')
dot.edge('D', 'RS', label='recovers from', style='dotted')

# Define a subgraph for the redundant capture devices
with dot.subgraph(name='cluster_capture_devices') as c:
    c.attr(style='filled', color='lightgrey')
    c.node('A')
    c.node('M')
    c.node('W')
    c.attr(label='Redundant Capture Devices')

# Render the graph to a file
dot.render('kafkacap_architecture')
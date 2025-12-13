import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(name='Open_Roberta_Lab_EV3_Architecture')
dot.attr(rankdir='TB')

# Add nodes for each layer
dot.node('ui', 'UI Layer\n(Brickman UI)', shape='box')
dot.node('service', 'Service Layer\n(roberta.lab.Service)', shape='box')
dot.node('network', 'Network Layer\n(roberta.lab.Connector)', shape='box')
dot.node('execution', 'Execution Layer\n(Code Execution)', shape='box')
dot.node('hal', 'HAL Layer\n(roberta.ev3.Hal)', shape='box')
dot.node('ev3dev', 'ev3dev Layer', shape='box')

# Add edges to show relationships and data flow
dot.edge('ui', 'service', 'DBus Communication')
dot.edge('service', 'network', 'Connection Management')
dot.edge('network', 'execution', 'Code Download & Execute')
dot.edge('execution', 'hal', 'Hardware Control')
dot.edge('hal', 'ev3dev', 'System Commands')

# Add key components as subgraphs
with dot.subgraph(name='cluster_components') as c:
    c.attr(label='Key Components')
    c.node('abort', 'AbortHandler\n(Key Press Monitor)', shape='box')
    c.node('gfx', 'GfxMode\n(Display Manager)', shape='box')
    c.edge('abort', 'execution', 'Program Control')
    c.edge('gfx', 'hal', 'Display Control')

# Set graph attributes for better visualization
dot.attr(fontsize='12')
dot.attr(pad='0.5')
dot.attr(splines='ortho')

# Render the graph
dot.render('open_roberta_architecture', format='png', cleanup=True)
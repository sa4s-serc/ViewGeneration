import graphviz

dot = graphviz.Digraph(comment='Open Roberta Lab EV3 Connector Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_ui') as c:
    c.attr(label='UI Layer', style='filled', color='lightgrey')
    c.node('brickman', 'Brickman UI', shape='rectangle')

with dot.subgraph(name='cluster_service') as c:
    c.attr(label='Service Layer', style='filled', color='lightblue')
    c.node('service', 'Service\n(roberta.lab.Service)', shape='rectangle')

with dot.subgraph(name='cluster_network') as c:
    c.attr(label='Network Layer', style='filled', color='lightgreen')
    c.node('connector', 'Connector\n(roberta.lab.Connector)', shape='rectangle')

with dot.subgraph(name='cluster_execution') as c:
    c.attr(label='Execution Layer', style='filled', color='lightyellow')
    c.node('execution', 'Code Execution\nEnvironment', shape='rectangle')

with dot.subgraph(name='cluster_hal') as c:
    c.attr(label='HAL Layer', style='filled', color='lightpink')
    c.node('hal', 'Hal\n(roberta.ev3.Hal)', shape='rectangle')

with dot.subgraph(name='cluster_ev3dev') as c:
    c.attr(label='ev3dev Layer', style='filled', color='lightcoral')
    c.node('ev3dev', 'ev3dev Library', shape='rectangle')

dot.node('server', 'Open Roberta Lab\nServer', shape='cylinder')
dot.node('abort', 'AbortHandler\n(roberta.lab.AbortHandler)', shape='rectangle')
dot.node('gfx', 'GfxMode\n(roberta.lab.GfxMode)', shape='rectangle')
dot.node('hardware', 'EV3 Hardware\n(Motors, Sensors, Display)', shape='box3d')

dot.edge('brickman', 'service', label='DBus', style='dashed')
dot.edge('service', 'connector', label='manages')
dot.edge('service', 'abort', label='manages')
dot.edge('service', 'gfx', label='manages')
dot.edge('connector', 'server', label='HTTP', dir='both')
dot.edge('connector', 'execution', label='downloads &\ninitiates')
dot.edge('execution', 'hal', label='uses')
dot.edge('hal', 'ev3dev', label='abstracts')
dot.edge('ev3dev', 'hardware', label='controls')
dot.edge('abort', 'execution', label='monitors\nfor abort', style='dashed')
dot.edge('gfx', 'hardware', label='manages\ndisplay', style='dashed')

dot.render('ev3_connector_architecture', format='png', cleanup=True)
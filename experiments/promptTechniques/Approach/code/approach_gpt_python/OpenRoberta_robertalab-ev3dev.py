from graphviz import Digraph

dot = Digraph(comment='Open Roberta Lab EV3 Connector Architecture', format='png')

# Define nodes
dot.node('UI', 'UI Layer\n(Brickman UI)', shape='rectangle', style='filled', color='lightblue')
dot.node('Service', 'Service Layer\n(roberta.lab.Service)', shape='rectangle', style='filled', color='lightgreen')
dot.node('Network', 'Network Layer\n(roberta.lab.Connector)', shape='rectangle', style='filled', color='lightyellow')
dot.node('Execution', 'Execution Layer\n(Connector)', shape='rectangle', style='filled', color='lightcoral')
dot.node('HAL', 'HAL Layer\n(roberta.ev3.Hal)', shape='rectangle', style='filled', color='lightgrey')
dot.node('ev3dev', 'ev3dev Layer\n(ev3dev.auto)', shape='rectangle', style='filled', color='lightpink')

dot.node('AbortHandler', 'AbortHandler\n(roberta.lab.AbortHandler)', shape='rectangle', style='filled', color='orange')
dot.node('GfxMode', 'GfxMode\n(roberta.lab.GfxMode)', shape='rectangle', style='filled', color='orange')

# Define edges
dot.edge('UI', 'Service', label='DBus Communication', dir='both')
dot.edge('Service', 'Network', label='Manage Connection\nand Delegation', dir='both')
dot.edge('Network', 'Execution', label='Code Download\nand Execution', dir='both')
dot.edge('Execution', 'HAL', label='Hardware Abstraction', dir='both')
dot.edge('HAL', 'ev3dev', label='Direct Interaction', dir='both')

dot.edge('Service', 'AbortHandler', label='Monitor Abort\nKey Presses')
dot.edge('Service', 'GfxMode', label='Manage Graphics\nMode')

# Add legend
with dot.subgraph() as s:
    s.attr(rank='min')
    s.node('Legend', 'Legend', shape='plaintext')
    s.node('Layer', 'Layer', shape='rectangle', style='filled')
    s.node('Component', 'Component', shape='rectangle', style='filled', color='orange')
    s.edge('Legend', 'Layer', label='Layers')
    s.edge('Legend', 'Component', label='Components')

dot.render('ev3_connector_architecture')
from graphviz import Digraph

dot = Digraph(comment='Open Roberta Lab EV3 Connector Architecture')

# Defining layers
dot.attr('node', shape='box', style='filled', fillcolor='lightgrey')
dot.node('UI', 'UI Layer: Brickman UI')

dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
dot.node('Service', 'Service Layer: roberta.lab.Service')

dot.attr('node', shape='box', style='filled', fillcolor='lightgreen')
dot.node('Network', 'Network Layer: roberta.lab.Connector')

dot.attr('node', shape='box', style='filled', fillcolor='lightyellow')
dot.node('Execution', 'Execution Layer: Connector')

dot.attr('node', shape='box', style='filled', fillcolor='lightcoral')
dot.node('HAL', 'HAL Layer: roberta.ev3.Hal')

dot.attr('node', shape='box', style='filled', fillcolor='lightpink')
dot.node('ev3dev', 'ev3dev Layer')

# Defining components
dot.attr('node', shape='ellipse', style='filled', fillcolor='white')
dot.node('ServiceObj', 'Service Object: DBus Interface')
dot.node('ConnectorObj', 'Connector: HTTP Requests')
dot.node('HalObj', 'Hal: EV3 Hardware Abstraction')
dot.node('AbortHandler', 'AbortHandler: Program Abortion')
dot.node('GfxMode', 'GfxMode: Graphics Management')

# Edges between layers
dot.edge('UI', 'Service', label='DBus Communication')
dot.edge('Service', 'Network', label='Manage Connections')
dot.edge('Network', 'Execution', label='Execute Code')
dot.edge('Execution', 'HAL', label='Hardware Control')
dot.edge('HAL', 'ev3dev', label='OS Interaction')

# Edges between components
dot.edge('Service', 'ServiceObj')
dot.edge('Network', 'ConnectorObj')
dot.edge('HAL', 'HalObj')
dot.edge('Service', 'AbortHandler')
dot.edge('Service', 'GfxMode')

# Save and render
dot.render('Open_Roberta_Lab_EV3_Connector_Architecture', format='png', cleanup=True)
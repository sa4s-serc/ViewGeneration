from graphviz import Digraph

dot = Digraph(comment='Autopatzer System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main layers
dot.node('ui', 'User Interface\n(React/Electron)')
dot.node('comm', 'Communication Layer\n(WebSocket/Perl)')
dot.node('control', 'Control Layer\n(Arduino/Teensy)')
dot.node('hardware', 'Hardware Layer')

# Add components within layers
with dot.subgraph(name='cluster_ui') as c:
    c.attr(label='UI Layer')
    c.node('lichess', 'Lichess API')
    c.node('game', 'Game Management')
    c.node('board', 'Board UI')

with dot.subgraph(name='cluster_hardware') as c:
    c.attr(label='Hardware Components')
    c.node('motors', 'Stepper Motors\n(NEMA17)')
    c.node('sensors', 'Hall Effect Sensors')
    c.node('magnet', 'Electromagnet')
    c.node('mux', 'Analog Multiplexers\n(CD4051B)')

# Add connections
dot.edge('ui', 'comm')
dot.edge('comm', 'control')
dot.edge('control', 'hardware')
dot.edge('lichess', 'game')
dot.edge('game', 'board')
dot.edge('control', 'motors')
dot.edge('control', 'magnet')
dot.edge('sensors', 'mux')
dot.edge('mux', 'control')

# Generate diagram
dot.render('autopatzer_architecture', view=True, format='png')
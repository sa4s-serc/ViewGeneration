from graphviz import Digraph

dot = Digraph(comment='AmnisIO Project Architecture')

# Define nodes
dot.node('TS', 'TypeScript Code')
dot.node('TW', 'Typewriter\n(Transpiler)')
dot.node('C', 'C Code')
dot.node('P', 'PlatformIO')
dot.node('CLI', 'AmnisIO CLI')
dot.node('Lib', 'Rivulet\n(Stream Library)')
dot.node('G', 'Gyrus\n(Board Abstraction)')
dot.node('HW', 'Arduino UNO\n(Hardware)')
dot.node('CMD', 'Commands\n(init, build, deploy)')

# Define edges
dot.edge('TS', 'TW', label='Transpile')
dot.edge('TW', 'C', label='Generate')
dot.edge('C', 'P', label='Build & Deploy')
dot.edge('P', 'HW', label='Flash Firmware')
dot.edge('CLI', 'CMD', label='Execute')
dot.edge('TS', 'Lib', label='Use')
dot.edge('TS', 'G', label='Use')
dot.edge('G', 'HW', label='Interface')

# Define graph attributes
dot.attr(rankdir='LR', size='8,5')
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.attr('edge', arrowsize='0.7')

# Render graph
dot.render('amnisio_architecture', format='png', cleanup=False)
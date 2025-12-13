from graphviz import Digraph

dot = Digraph(comment='AmnisIO Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('ts_code', 'TypeScript Code\n(IoT Application)')
dot.node('typewriter', 'Typewriter\nTranspiler')
dot.node('c_code', 'Generated C Code')
dot.node('platform_io', 'PlatformIO')
dot.node('rivulet', 'Rivulet\nStream Library')
dot.node('gyrus', 'Gyrus\nBoard Abstraction')
dot.node('cli', 'AmnisIO CLI')
dot.node('device', 'Arduino UNO')

# Add subgraph for configuration
with dot.subgraph(name='cluster_config') as config:
    config.attr(label='Configuration Layer')
    config.node('config_files', 'Config Files\n(.amnisio.config.json)')
    config.node('board_config', 'Board Configs\n(arduino-uno.ts)')

# Add edges
dot.edge('ts_code', 'typewriter', 'transpile')
dot.edge('typewriter', 'c_code', 'generate')
dot.edge('c_code', 'platform_io', 'build')
dot.edge('platform_io', 'device', 'deploy')
dot.edge('rivulet', 'c_code', 'provides streams')
dot.edge('gyrus', 'c_code', 'provides hardware\nabstraction')
dot.edge('cli', 'typewriter', 'invokes')
dot.edge('cli', 'platform_io', 'manages')
dot.edge('config_files', 'cli', 'configures')
dot.edge('board_config', 'gyrus', 'defines')

# Print the dot source
print(dot.source)

# Render the diagram
dot.render('amnisio_architecture', format='png', cleanup=True)
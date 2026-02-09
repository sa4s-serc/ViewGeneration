import graphviz

dot = graphviz.Digraph(comment='AmnisIO Architecture')
dot.attr(rankdir='TB', size='8,8')

# Developer Layer
with dot.subgraph(name='cluster_developer') as c:
    c.attr(label='Developer Layer', style='filled', color='lightblue')
    c.node('typescript', 'TypeScript Code', shape='ellipse')
    c.node('cli', 'AmnisIO CLI', shape='box')
    c.node('config', 'Configuration Files', shape='note')

# Transpilation Layer
with dot.subgraph(name='cluster_transpilation') as c:
    c.attr(label='Transpilation Layer', style='filled', color='lightgreen')
    c.node('typewriter', 'TypeWriter Transpiler', shape='component')
    c.node('rivulet', 'Rivulet Stream Library', shape='component')

# Platform Layer
with dot.subgraph(name='cluster_platform') as c:
    c.attr(label='Platform Layer', style='filled', color='lightyellow')
    c.node('platformio', 'PlatformIO', shape='box')
    c.node('gyrus', 'Gyrus Board Abstraction', shape='component')

# Hardware Layer
with dot.subgraph(name='cluster_hardware') as c:
    c.attr(label='Hardware Layer', style='filled', color='lightcoral')
    c.node('arduino', 'Arduino UNO', shape='box3d')
    c.node('peripherals', 'Hardware Peripherals', shape='box3d')

# Edges
dot.edge('typescript', 'cli', label='commands')
dot.edge('cli', 'typewriter', label='transpiles to')
dot.edge('typewriter', 'rivulet', label='uses')
dot.edge('cli', 'platformio', label='builds/deploys')
dot.edge('platformio', 'gyrus', label='abstracts')
dot.edge('gyrus', 'arduino', label='runs on')
dot.edge('arduino', 'peripherals', label='controls')
dot.edge('config', 'cli', label='configures', style='dashed')
dot.edge('config', 'gyrus', label='configures', style='dashed')

dot.render('amnisio_architecture', format='png', cleanup=True)
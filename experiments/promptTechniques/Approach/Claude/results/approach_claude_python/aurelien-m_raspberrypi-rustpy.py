import graphviz

# Create a new directed graph
g = graphviz.Digraph('G', filename='architecture.png', format='png')
g.attr(rankdir='TB')

# Define clusters/subgraphs
with g.subgraph(name='cluster_web') as c:
    c.attr(label='Web Layer', style='filled', color='lightgrey')
    c.node('web_server', 'Web Server\n(Rust/Rocket)', shape='box')
    c.node('auth', 'Authentication', shape='box')
    c.node('websocket', 'WebSocket Handler', shape='box')
    c.node('templates', 'HTML Templates', shape='box')
    c.node('static', 'Static Files', shape='box')

with g.subgraph(name='cluster_control') as c:
    c.attr(label='Control Layer', style='filled', color='lightblue')
    c.node('python_ctrl', 'Python Controller', shape='box')
    c.node('settings', 'Settings Manager', shape='box')
    c.node('led_control', 'LED Control', shape='box')
    c.node('bluetooth', 'Bluetooth\nCommunication', shape='box')

with g.subgraph(name='cluster_hardware') as c:
    c.attr(label='Hardware Layer', style='filled', color='lightgreen')
    c.node('rust_lib', 'Rust Hardware Library', shape='box')
    c.node('hardware', 'Raspberry Pi Hardware', shape='box')

# Add edges
g.edge('web_server', 'auth')
g.edge('web_server', 'websocket')
g.edge('web_server', 'templates')
g.edge('web_server', 'static')
g.edge('web_server', 'python_ctrl')
g.edge('python_ctrl', 'settings')
g.edge('python_ctrl', 'led_control')
g.edge('python_ctrl', 'bluetooth')
g.edge('python_ctrl', 'rust_lib')
g.edge('rust_lib', 'hardware')

# Add edge labels for key interactions
g.edge('websocket', 'python_ctrl', 'real-time updates')
g.edge('python_ctrl', 'led_control', 'mode control')
g.edge('led_control', 'rust_lib', 'hardware commands')

# Set graph attributes
g.attr(label='Raspberry Pi Hardware Control System Architecture')
g.attr(fontsize='16')

# Render the graph
g.render(filename='architecture', view=True, cleanup=True)
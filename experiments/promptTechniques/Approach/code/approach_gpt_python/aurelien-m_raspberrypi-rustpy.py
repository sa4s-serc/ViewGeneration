from graphviz import Digraph

dot = Digraph(comment='Raspberry Pi Hardware Control System Architecture')

# Define styles for the nodes
styles = {
    'rust': {'shape': 'box', 'style': 'filled', 'fillcolor': '#ffcccb'},
    'python': {'shape': 'box', 'style': 'filled', 'fillcolor': '#add8e6'},
    'web': {'shape': 'box', 'style': 'filled', 'fillcolor': '#90ee90'},
    'bluetooth': {'shape': 'ellipse', 'style': 'filled', 'fillcolor': '#f0e68c'}
}

# Add nodes with styles
dot.node('RUST', 'Rust Library\n(rppal, GPIO)', **styles['rust'])
dot.node('PY', 'Python Interface\n(rpipy.py)', **styles['python'])
dot.node('WS', 'Web Server\n(Rocket Framework)', **styles['web'])
dot.node('BT', 'Bluetooth\n(Communication)', **styles['bluetooth'])

# Add edges to represent interactions
dot.edge('RUST', 'PY', 'Function Call\n(Adapter Pattern)')
dot.edge('PY', 'WS', 'API Call\n(Facade Pattern)')
dot.edge('WS', 'BT', 'Data Exchange\n(Observer Pattern)')

# Add web interface and client-server relationship
dot.node('GUI', 'Web Interface', **styles['web'])
dot.node('CLIENT', 'Web Client\n(Browser)', **styles['web'])
dot.edge('CLIENT', 'GUI', 'HTTP Request')
dot.edge('GUI', 'WS', 'WebSocket\nCommunication')

# Add hardware components
dot.node('LED', 'LEDs', **styles['rust'])
dot.edge('RUST', 'LED', 'GPIO Control')

# Drawing the architecture
print(dot.source)
dot.render('raspberry_pi_hardware_control_system_architecture', format='png', cleanup=True)
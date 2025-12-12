from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ZID-Automat Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgray')

# Main components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components', style='rounded', bgcolor='lightblue')
    core.node('main', 'Main123\nCore Controller')
    core.node('borrow', 'BorrowM\nBorrowing Logic')
    core.node('config', 'Configuration.json')

# Hardware interfaces
with dot.subgraph(name='cluster_hardware') as hw:
    hw.attr(label='Hardware Interfaces', style='rounded', bgcolor='lightgreen')
    hw.node('qr', 'QRCodeReader\nSerial Communication')
    hw.node('eject', 'Eject\nItem Dispensing')
    hw.node('screen', 'ScreenOutput\nLCD Display')
    hw.node('led', 'NeoPixel\nLED Strip')

# Backend communication
with dot.subgraph(name='cluster_backend') as backend:
    backend.attr(label='Backend Services', style='rounded', bgcolor='lightyellow')
    backend.node('api', 'Requests\nBackend API')
    backend.node('data', 'DataCollect\nEvent Logging')

# Relationships
dot.edge('main', 'borrow', 'orchestrates')
dot.edge('main', 'config', 'loads')
dot.edge('main', 'led', 'controls')

dot.edge('borrow', 'qr', 'reads codes')
dot.edge('borrow', 'eject', 'triggers ejection')
dot.edge('borrow', 'screen', 'updates display')
dot.edge('borrow', 'api', 'validates QR codes')
dot.edge('borrow', 'data', 'logs events')

dot.edge('api', 'data', 'sends logs')

# Hardware connections
with dot.subgraph(name='cluster_connections') as conn:
    conn.attr(label='Physical Connections', style='rounded', bgcolor='lightpink')
    conn.node('serial', 'Serial Port')
    conn.node('gpio', 'GPIO Pins')
    conn.node('i2c', 'I2C Bus')

dot.edge('qr', 'serial', 'uses')
dot.edge('eject', 'gpio', 'controls')
dot.edge('screen', 'i2c', 'communicates')

# Save the diagram
dot.render('zid_automat_architecture', format='png', cleanup=True)
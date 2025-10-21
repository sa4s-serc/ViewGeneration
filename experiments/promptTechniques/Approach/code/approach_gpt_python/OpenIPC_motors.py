from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='OpenIPC Motors Architecture')

# Add nodes for each architectural layer
dot.node('HW', 'Hardware Layer', shape='rect', style='filled', color='lightgrey')
dot.node('KDL', 'Kernel Driver Layer', shape='rect', style='filled', color='lightblue')
dot.node('DWL', 'Driver Wrapper Layer', shape='rect', style='filled', color='lightgreen')
dot.node('DL', 'Daemon Layer', shape='rect', style='filled', color='lightyellow')
dot.node('AL', 'Application Layer', shape='rect', style='filled', color='lightcoral')

# Add sub-nodes for hardware components
dot.node('GPIO', 'GPIO Control', shape='rect')
dot.node('I2C', 'I2C Motor Controller', shape='rect')
dot.node('SPI', 'SPI Motor Controller', shape='rect')
dot.node('UART', 'UART (Pelco-D)', shape='rect')

# Add sub-nodes for Driver Wrapper Layer
dot.node('DW_GPIO', 'GPIO Driver Wrapper', shape='rect')
dot.node('DW_I2C', 'I2C Driver Wrapper', shape='rect')
dot.node('DW_SPI', 'SPI Driver Wrapper', shape='rect')
dot.node('DW_UART', 'UART Driver Wrapper', shape='rect')

# Add sub-nodes for Daemon Layer
dot.node('MD', 'Motors Daemon', shape='rect')

# Add sub-nodes for Application Layer
dot.node('CA', 'Camera Applications', shape='rect')

# Connect hardware components to Kernel Driver Layer
dot.edge('GPIO', 'KDL', label='Control')
dot.edge('I2C', 'KDL', label='Control')
dot.edge('SPI', 'KDL', label='Control')
dot.edge('UART', 'KDL', label='Control')

# Connect Kernel Driver Layer to Driver Wrapper Layer
dot.edge('KDL', 'DW_GPIO', label='Abstract')
dot.edge('KDL', 'DW_I2C', label='Abstract')
dot.edge('KDL', 'DW_SPI', label='Abstract')
dot.edge('KDL', 'DW_UART', label='Abstract')

# Connect Driver Wrapper Layer to Daemon Layer
dot.edge('DWL', 'MD', label='Manage')

# Connect Daemon Layer to Application Layer
dot.edge('MD', 'CA', label='API Access')

# Group nodes into layers
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Hardware Components')
    c.node('GPIO')
    c.node('I2C')
    c.node('SPI')
    c.node('UART')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Kernel Driver Layer')
    c.node('KDL')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Driver Wrapper Layer')
    c.node('DW_GPIO')
    c.node('DW_I2C')
    c.node('DW_SPI')
    c.node('DW_UART')

with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Daemon Layer')
    c.node('MD')

with dot.subgraph(name='cluster_4') as c:
    c.attr(label='Application Layer')
    c.node('CA')

# Render the diagram to a file
dot.render('openipc_motors_architecture', format='png', cleanup=True)
from graphviz import Digraph

dot = Digraph(comment='OpenIPC Motors Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add layers
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Application Layer')
    c.node('camera_app', 'Camera Applications')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Daemon Layer')
    c.node('motors_daemon', 'Motors Daemon')
    c.node('api', 'Unified API')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Driver Wrapper Layer')
    c.node('camhi', 'CamHI Wrapper')
    c.node('i2c', 'I2C Wrapper')
    c.node('uart', 'UART Wrapper')
    c.node('an41908a', 'AN41908A Wrapper')

with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Kernel Driver Layer')
    c.node('kmotor', 'Motor Kernel Module')
    c.node('i2c_dev', 'I2C Device Driver')
    c.node('spi_dev', 'SPI Device Driver')
    c.node('uart_dev', 'UART Device Driver')

with dot.subgraph(name='cluster_4') as c:
    c.attr(label='Hardware Layer')
    c.node('motor_hw', 'Motor Hardware')

# Add edges
dot.edge('camera_app', 'motors_daemon')
dot.edge('motors_daemon', 'api')
dot.edge('api', 'camhi')
dot.edge('api', 'i2c')
dot.edge('api', 'uart')
dot.edge('api', 'an41908a')
dot.edge('camhi', 'kmotor')
dot.edge('i2c', 'i2c_dev')
dot.edge('uart', 'uart_dev')
dot.edge('an41908a', 'spi_dev')
dot.edge('kmotor', 'motor_hw')
dot.edge('i2c_dev', 'motor_hw')
dot.edge('uart_dev', 'motor_hw')
dot.edge('spi_dev', 'motor_hw')

dot.render('openipc_motors_architecture', view=True, format='png')
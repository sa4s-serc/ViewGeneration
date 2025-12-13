from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ZID-Automat Controller Software Architecture')

# Define nodes with different shapes
dot.node('A', 'Main123', shape='rectangle')
dot.node('B', 'BorrowM', shape='rectangle')
dot.node('C', 'Requestsi', shape='rectangle')
dot.node('D', 'QRCodeReader', shape='rectangle')
dot.node('E', 'Eject', shape='rectangle')
dot.node('F', 'DataCollect', shape='rectangle')
dot.node('G', 'ScreenOutput', shape='rectangle')
dot.node('H', 'mp_i2c_lcd1602', shape='rectangle')
dot.node('I', 'Configuration', shape='ellipse')
dot.node('J', 'Backend Server', shape='ellipse')

# Define edges with arrows to show communication and relationships
dot.edge('A', 'B', label='orchestrates', arrowhead='normal')
dot.edge('B', 'C', label='uses', arrowhead='normal')
dot.edge('B', 'D', label='reads', arrowhead='normal')
dot.edge('B', 'E', label='controls', arrowhead='normal')
dot.edge('B', 'F', label='logs', arrowhead='normal')
dot.edge('B', 'G', label='displays', arrowhead='normal')
dot.edge('G', 'H', label='managed by', arrowhead='normal')
dot.edge('A', 'I', label='loads', arrowhead='normal')
dot.edge('C', 'J', label='interacts', arrowhead='normal')

# Render the graph
dot.render('zid_automat_controller_architecture', view=True, format='png')
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Multi-Component System', format='png')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')

# Define nodes for main components
dot.node('3D', '3D Rendering & Visualization\n(Potree, Three.js)', fillcolor='lightblue')
dot.node('Robotic', 'Robotic Control & Sensing\n(ROS Integration)', fillcolor='lightgreen')
dot.node('Geometric', 'Geometric Data Handling\n(CZML Processing)', fillcolor='lightyellow')

# Define nodes for key libraries and utilities
dot.node('Three.js', 'Three.js', fillcolor='lightblue')
dot.node('Potree', 'Potree', fillcolor='lightblue')
dot.node('ROS', 'ROS', fillcolor='lightgreen')
dot.node('CZML', 'CZML', fillcolor='lightyellow')

# Define nodes for key components within subsystems
dot.node('PointCloud', 'PointCloud Material', fillcolor='lightblue')
dot.node('Shader', 'Shader System', fillcolor='lightblue')
dot.node('Robot', 'Robot Control', fillcolor='lightgreen')
dot.node('Sensor', 'Sensor Data Acquisition', fillcolor='lightgreen')
dot.node('ICP', 'Iterative Closest Point', fillcolor='lightgreen')
dot.node('CzmlDataSource', 'CzmlDataSource', fillcolor='lightyellow')
dot.node('Animations', 'Animations', fillcolor='lightyellow')

# Define edges to represent communication between components
dot.edge('3D', 'Three.js')
dot.edge('3D', 'Potree')
dot.edge('Three.js', 'PointCloud')
dot.edge('Three.js', 'Shader')
dot.edge('Robotic', 'ROS')
dot.edge('Robotic', 'Robot')
dot.edge('Robotic', 'Sensor')
dot.edge('Robotic', 'ICP')
dot.edge('Geometric', 'CZML')
dot.edge('Geometric', 'CzmlDataSource')
dot.edge('Geometric', 'Animations')

# Define edges for communication between main components
dot.edge('3D', 'Robotic', label='Data Exchange')
dot.edge('3D', 'Geometric', label='Data Exchange')
dot.edge('Robotic', 'Geometric', label='Sensor Data')

# Render the graph
dot.render('multi_component_system', view=True)
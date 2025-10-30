from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Multi-Component System Architecture')

# Add nodes for 3D Rendering and Visualization Core (Potree, Three.js)
dot.node('Three.js', 'Three.js\n(Core Rendering)', shape='rectangle', style='filled', color='lightblue')
dot.node('Potree', 'Potree\n(Point Cloud Rendering)', shape='rectangle', style='filled', color='lightblue')
dot.node('LAS/LAZ Decoders', 'LAS/LAZ Decoders\n(Data Loading)', shape='rectangle', style='filled', color='lightblue')

# Add nodes for Robotic Control and Sensing (ROS Integration)
dot.node('Robot', 'Robot Control', shape='rectangle', style='filled', color='lightgreen')
dot.node('Sensor', 'Sensor Data Acquisition', shape='rectangle', style='filled', color='lightgreen')
dot.node('ICP', 'Iterative Closest Point\n(Point Cloud Registration)', shape='rectangle', style='filled', color='lightgreen')

# Add nodes for Geometric Data Handling and CZML Processing
dot.node('CzmlDataSource', 'CZML Data Source', shape='rectangle', style='filled', color='lightyellow')
dot.node('CZML Processing', 'CZML Processing\n(Time-Dynamic Objects)', shape='rectangle', style='filled', color='lightyellow')

# Add edges to represent communication and data flow
dot.edge('Three.js', 'Potree', label='integrates')
dot.edge('Potree', 'LAS/LAZ Decoders', label='uses')
dot.edge('Robot', 'Sensor', label='controls')
dot.edge('Sensor', 'ICP', label='provides data for')
dot.edge('CzmlDataSource', 'CZML Processing', label='feeds')

# Render the graph to a file
dot.render('multi_component_system_architecture', format='png', cleanup=True)
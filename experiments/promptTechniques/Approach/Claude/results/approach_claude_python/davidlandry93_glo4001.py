import graphviz

# Create a new directed graph
dot = graphviz.Digraph(
    'architecture_view',
    comment='Software Architecture View',
    engine='dot'
)

# Graph attributes
dot.attr(rankdir='TB', splines='ortho')
dot.attr(fontname='Arial', compound='true')

# Global node attributes
dot.attr('node', shape='box', style='rounded', fontname='Arial', margin='0.3')

# Create main components cluster
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core System Components', style='rounded', color='blue')
    
    # 3D Rendering components
    core.node('threejs', 'Three.js\nRendering Engine')
    core.node('potree', 'Potree\nPoint Cloud Renderer')
    core.node('shader', 'Shader System')
    core.edge('potree', 'threejs')
    core.edge('shader', 'threejs')

# Create robotics cluster
with dot.subgraph(name='cluster_robotics') as robotics:
    robotics.attr(label='Robotics Control', style='rounded', color='green')
    
    robotics.node('ros', 'ROS Integration')
    robotics.node('sensors', 'Sensor\nData Acquisition')
    robotics.node('control', 'Robot Control')
    robotics.edge('sensors', 'control')
    robotics.edge('control', 'ros')

# Create data handling cluster
with dot.subgraph(name='cluster_data') as data:
    data.attr(label='Data Processing', style='rounded', color='red')
    
    data.node('pointcloud', 'Point Cloud\nProcessing')
    data.node('czml', 'CZML Parser')
    data.node('icp', 'ICP Algorithm')
    data.edge('pointcloud', 'icp')

# Cross-cluster connections
dot.edge('sensors', 'pointcloud')
dot.edge('pointcloud', 'potree')
dot.edge('czml', 'threejs')
dot.edge('ros', 'control')

# Add system services
dot.node('plugins', 'Plugin System')
dot.node('events', 'Event System')

# Connect services
dot.edge('plugins', 'threejs', 'extends')
dot.edge('events', 'threejs', 'notifies')
dot.edge('events', 'control', 'commands')

# Save the diagram
dot.render('architecture_view', format='png', cleanup=True)
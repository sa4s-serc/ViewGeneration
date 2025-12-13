import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='LARCC Robotic System Architecture')
dot.attr(rankdir='TB')

# Configure global node and edge styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial', fontsize='10')
dot.attr('edge', fontname='Arial', fontsize='9')

# Define main system components
with dot.subgraph(name='cluster_control') as control:
    control.attr(label='Control Layer', style='rounded', color='blue')
    control.node('ur10e', 'UR10e Robot Control\nURCap & RS485')
    control.node('moveit', 'MoveIt! Integration\nPath Planning & Control')
    control.node('kinematics', 'Robot Kinematics\nIK/FK Solvers')

with dot.subgraph(name='cluster_perception') as perception:
    perception.attr(label='Perception Layer', style='rounded', color='green')
    perception.node('realsense', 'RealSense Camera\nRGB-D Tracking')
    perception.node('vision', 'Computer Vision\nObject Detection')

with dot.subgraph(name='cluster_description') as description:
    description.attr(label='System Description', style='rounded', color='orange')
    description.node('workcell', 'LARCC Workcell\nURDF/Xacro Models')
    description.node('models', '3D Model Definitions\nMesh & Material Data')

# Add ROS core as central component
dot.node('ros', 'ROS Core\nCommunication Backend', shape='doubleoctagon', color='red')

# Define connections
# Control layer connections
dot.edge('ros', 'ur10e', 'Robot Control')
dot.edge('ros', 'moveit', 'Planning')
dot.edge('moveit', 'kinematics', 'Solve IK/FK')
dot.edge('ur10e', 'kinematics', 'Joint States')

# Perception layer connections
dot.edge('ros', 'realsense', 'Sensor Data')
dot.edge('realsense', 'vision', 'RGB-D Data')
dot.edge('vision', 'moveit', 'Object Poses')

# Description layer connections
dot.edge('ros', 'workcell', 'Cell Config')
dot.edge('workcell', 'models', 'Geometry Data')
dot.edge('models', 'moveit', 'Collision Models')

# Set graph title
dot.attr(label='LARCC Robotic System Architecture\nROS-based Component Architecture', labelloc='t', fontsize='14')

# Render the graph
dot.render('larcc_architecture', format='png', cleanup=True)
from graphviz import Digraph

dot = Digraph(comment='Self-Driving Car ROS Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Create main subsystems
dot.node('perception', 'Perception\n(Traffic Light Detection)')
dot.node('planning', 'Planning\n(Waypoint Management)')
dot.node('control', 'Control\n(DBW)')
dot.node('bridge', 'Bridge Node\n(Simulator Interface)')

# Create specific components
with dot.subgraph(name='cluster_perception') as p:
    p.attr(label='Perception Components')
    p.node('tl_detector', 'Traffic Light\nDetector')
    p.node('tl_classifier', 'Traffic Light\nClassifier')
    p.node('camera_info', 'Camera Info\nPublisher')

with dot.subgraph(name='cluster_planning') as pl:
    pl.attr(label='Planning Components')
    pl.node('waypoint_loader', 'Waypoint\nLoader')
    pl.node('waypoint_updater', 'Waypoint\nUpdater')
    pl.node('waypoint_follower', 'Waypoint\nFollower')

with dot.subgraph(name='cluster_control') as c:
    c.attr(label='Control Components')
    c.node('dbw_node', 'DBW Node')
    c.node('pid', 'PID Controller')
    c.node('yaw_controller', 'Yaw Controller')
    c.node('lowpass', 'Lowpass Filter')

# Define connections
dot.edge('tl_detector', 'tl_classifier')
dot.edge('camera_info', 'tl_detector')
dot.edge('waypoint_loader', 'waypoint_updater')
dot.edge('waypoint_updater', 'waypoint_follower')
dot.edge('waypoint_follower', 'dbw_node')
dot.edge('dbw_node', 'pid')
dot.edge('dbw_node', 'yaw_controller')
dot.edge('dbw_node', 'lowpass')

# Connect main subsystems
dot.edge('perception', 'planning', 'Traffic Light Status')
dot.edge('planning', 'control', 'Waypoints')
dot.edge('bridge', 'perception', 'Camera Images')
dot.edge('bridge', 'planning', 'Vehicle Position')
dot.edge('control', 'bridge', 'Control Commands')

# Set graph attributes
dot.attr(label='Self-Driving Car ROS Architecture\nUdacity/CARLA Project', labelloc='t')
dot.attr(fontsize='20')

# Save the diagram
dot.render('self_driving_car_architecture', format='png', cleanup=True)
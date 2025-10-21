from graphviz import Digraph

dot = Digraph(comment='Self-Driving Car ROS Project', format='png')

# Define nodes for each component
dot.node('TL', 'Traffic Light Detection\n(tl_classifier.py)')
dot.node('CI', 'Camera Info Publisher\n(camera_info_publisher)')
dot.node('WL', 'Waypoint Loader\n(waypoint_loader.py)')
dot.node('WU', 'Waypoint Updater\n(waypoint_updater.py)')
dot.node('WF', 'Waypoint Follower\n(libwaypoint_follower.cpp)')
dot.node('DBW', 'Twist Controller (DBW)\n(dbw_node.py)')
dot.node('PID', 'PID Controller\n(pid.py)')
dot.node('YC', 'Yaw Controller\n(yaw_controller.py)')
dot.node('LP', 'LowPass Filter\n(lowpass.py)')
dot.node('BR', 'Bridge Node\n(server.py, bridge.py)')

# Define the infrastructure
dot.node('Sim', 'Udacity Simulator')
dot.node('Carla', 'CARLA Real Car')

# Define edges for communication
dot.edge('TL', 'WU', label='Traffic Light Status')
dot.edge('CI', 'TL', label='Camera Calibration')
dot.edge('WL', 'WU', label='Waypoints')
dot.edge('WU', 'WF', label='Adjusted Waypoints')
dot.edge('WF', 'DBW', label='Target Velocities')
dot.edge('DBW', 'PID', label='Throttle Control')
dot.edge('PID', 'YC', label='Steering Control')
dot.edge('YC', 'LP', label='Filtered Steering')
dot.edge('BR', 'Sim', label='Connects to')
dot.edge('BR', 'Carla', label='Connects to')

# Define clusters for perceptual organization
with dot.subgraph(name='cluster_perception') as c:
    c.attr(label='Perception')
    c.node('TL')
    c.node('CI')

with dot.subgraph(name='cluster_planning') as c:
    c.attr(label='Planning')
    c.node('WL')
    c.node('WU')
    c.node('WF')

with dot.subgraph(name='cluster_control') as c:
    c.attr(label='Control')
    c.node('DBW')
    c.node('PID')
    c.node('YC')
    c.node('LP')

with dot.subgraph(name='cluster_infrastructure') as c:
    c.attr(label='Infrastructure')
    c.node('BR')
    c.node('Sim')
    c.node('Carla')

# Render the diagram
dot.render('self_driving_car_ros_project')
from graphviz import Digraph

dot = Digraph(comment='Software Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Core Components
dot.node('eigen', 'Eigen Library\nLinear Algebra Core')
dot.node('json', 'nlohmann::json\nJSON Processing')
dot.node('uws', 'µWebSockets\nReal-time Communication')
dot.node('tf', 'TensorFlow/Keras\nTraffic Light Classifier')
dot.node('ros', 'ROS Framework')

# Subsystems
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Linear Algebra Subsystem')
    c.node('matrix_ops', 'Matrix Operations')
    c.node('decomp', 'Matrix Decompositions')
    c.node('solvers', 'Linear Solvers')
    c.node('geo', 'Geometric Transforms')

# Traffic Light Classification
with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Traffic Light Classification')
    c.node('cnn', 'CNN Model')
    c.node('classifier', 'State Classifier')
    c.node('cuda', 'CUDA Acceleration')

# Autonomous Driving
with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Autonomous Driving')
    c.node('waypoint', 'Waypoint Handler')
    c.node('traffic', 'Traffic Detection')
    c.node('control', 'DBW Controller')

# Define relationships
dot.edge('eigen', 'matrix_ops')
dot.edge('eigen', 'decomp')
dot.edge('eigen', 'solvers')
dot.edge('eigen', 'geo')
dot.edge('tf', 'cnn')
dot.edge('cnn', 'classifier')
dot.edge('cuda', 'cnn')
dot.edge('ros', 'waypoint')
dot.edge('ros', 'traffic')
dot.edge('ros', 'control')
dot.edge('classifier', 'traffic')
dot.edge('json', 'waypoint')
dot.edge('uws', 'control')

# Set graph attributes
dot.attr(fontname='Helvetica')
dot.attr('node', fontname='Helvetica')
dot.attr('edge', fontname='Helvetica')

# Generate diagram
dot.render('architecture_view', format='png', cleanup=True)
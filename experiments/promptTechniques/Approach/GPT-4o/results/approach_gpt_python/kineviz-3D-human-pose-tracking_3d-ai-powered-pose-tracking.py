from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='3D Human Pose Tracking System')

# Define nodes for each key component
dot.node('C1', 'Webcam Clients (Orthogonal Setup)', shape='rectangle')
dot.node('C2', 'Node.js Server', shape='rectangle')
dot.node('C3', 'TensorFlow.js (PoseNet/MoveNet)', shape='rectangle')
dot.node('C4', 'Socket.IO', shape='rectangle')
dot.node('C5', 'Kineviz GraphXR', shape='rectangle')

# Define edges to show communication and data flow
dot.edge('C1', 'C2', label='Real-time 2D Pose Data', dir='both')
dot.edge('C2', 'C3', label='3D Pose Estimation')
dot.edge('C2', 'C4', label='Data Distribution', dir='both')
dot.edge('C2', 'C5', label='Broadcast 3D Skeleton Data')

# Add legend
dot.node('L1', 'Legend', shape='plaintext')
dot.node('L2', 'Components: Rectangle', shape='plaintext')
dot.node('L3', 'Bidirectional Data Flow: Double-headed Arrows', shape='plaintext')

dot.edge('L1', 'L2', style='invis')
dot.edge('L1', 'L3', style='invis')

# Render the diagram
dot.render('3d_human_pose_tracking_system', format='png', cleanup=True)
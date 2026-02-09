import graphviz as gv

dot = gv.Digraph(name='3D_Pose_Tracking_Architecture', 
                 comment='Architectural view of 3D Human Pose Tracking System',
                 format='png')

# Set diagram attributes
dot.attr(rankdir='TB', splines='ortho')

# Add clusters/subgraphs
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Client Side', style='rounded', color='lightblue')
    c.node('webcam1', 'Webcam 1\nPoseNet/MoveNet', shape='rectangle')
    c.node('webcam2', 'Webcam 2\nPoseNet/MoveNet', shape='rectangle')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Server Side', style='rounded', color='lightgreen')
    c.node('server', 'Node.js Server\nSocket.IO', shape='rectangle')
    c.node('pose_proc', '3D Pose\nReconstruction', shape='rectangle')
    c.node('data_viz', 'Data\nVisualization', shape='rectangle')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Client Applications', style='rounded', color='lightpink')
    c.node('receiver', 'Receiver\nApplication', shape='rectangle')
    c.node('graphxr', 'GraphXR\nVisualization', shape='rectangle')

# Add edges
dot.edge('webcam1', 'server', 'skeleton data')
dot.edge('webcam2', 'server', 'skeleton data')
dot.edge('server', 'pose_proc', 'raw 2D poses')
dot.edge('pose_proc', 'data_viz', '3D pose data')
dot.edge('data_viz', 'receiver', 'processed data')
dot.edge('data_viz', 'graphxr', 'visualization data')

# Generate diagram
dot.render('3d_pose_tracking_architecture', view=True, cleanup=True)
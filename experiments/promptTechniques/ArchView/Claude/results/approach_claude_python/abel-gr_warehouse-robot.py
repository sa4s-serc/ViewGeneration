import graphviz

# Create a new directed graph
dot = graphviz.Digraph('warehouse_robot_architecture', 
                       comment='Warehouse Robot Simulation Architecture',
                       format='png')

# Set graph attributes
dot.attr(rankdir='TB', splines='ortho')
dot.attr('node', shape='box', style='rounded')

# Create clusters/subgraphs for main components
with dot.subgraph(name='cluster_0') as s0:
    s0.attr(label='Unity Environment', style='rounded', color='blue')
    s0.node('prefabs', 'Warehouse Elements\n(Drop Zone, Shelves, Robot)')
    s0.node('unity_scripts', 'MonoBehaviour Scripts')
    s0.node('transforms', 'Transforms & Colliders')
    
    # Add relationships within Unity cluster
    s0.edge('prefabs', 'transforms')
    s0.edge('unity_scripts', 'transforms')

with dot.subgraph(name='cluster_1') as s1:
    s1.attr(label='CoppeliaSim Environment', style='rounded', color='green')
    s1.node('sim_api', 'Remote API (sim.py)')
    s1.node('robot_control', 'Robot Control\n(robot.py)')
    s1.node('kinematics', 'Inverse Kinematics\n(cinematica_inversa.ipynb)')
    s1.node('ocr', 'OCR Pipeline\n(OCR_Lite.py)')
    
    # Add relationships within CoppeliaSim cluster
    s1.edge('sim_api', 'robot_control')
    s1.edge('robot_control', 'kinematics')
    s1.edge('robot_control', 'ocr')

with dot.subgraph(name='cluster_2') as s2:
    s2.attr(label='Web Interface', style='rounded', color='red')
    s2.node('web_ui', 'User Interface')
    s2.node('speech', 'Speech-to-Text\n(Cloud Functions)')
    s2.node('recorder', 'Audio Recording\n(recorderjs)')
    
    # Add relationships within Web Interface cluster
    s2.edge('web_ui', 'recorder')
    s2.edge('recorder', 'speech')

# Add inter-cluster relationships
dot.edge('transforms', 'sim_api', 'Environment State')
dot.edge('robot_control', 'transforms', 'Robot State')
dot.edge('speech', 'robot_control', 'Voice Commands')

# Set graph title
dot.attr(label='Warehouse Robot Simulation Architecture\n', labelloc='t', fontsize='20')

# Render the graph
dot.render('warehouse_robot_architecture', view=True, cleanup=True)
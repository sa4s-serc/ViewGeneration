from graphviz import Digraph

# Initialize a directed graph
dot = Digraph(comment='UR10e Robotic Workcell Architecture')

# Define sub-systems
dot.node('A', 'UR10e Control Interface', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'MoveIt! Integration', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('C', 'Robot Kinematics', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('D', 'LARCC Workcell Description', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('E', 'RealSense Camera Support', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F', '3D Model Definitions', shape='rectangle', style='filled', fillcolor='lightblue')

# Define communication paths (edges)
dot.edge('A', 'B', label='Path Planning', arrowhead='normal')
dot.edge('B', 'C', label='Kinematics Solvers', arrowhead='normal')
dot.edge('C', 'D', label='Simulate & Visualize', arrowhead='normal')
dot.edge('D', 'E', label='Capture Data', arrowhead='normal')
dot.edge('E', 'F', label='Model Representation', arrowhead='normal')
dot.edge('F', 'A', label='Control Feedback', arrowhead='normal')

# Render the graph
dot.format = 'png'
dot.render('ur10e_workcell_architecture', view=True)
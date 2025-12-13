from graphviz import Digraph

dot = Digraph(comment='TALOS Robot Locomotion Controller')

# Components
dot.node('A', 'Bipedal Locomotion Control')
dot.node('B', 'Whole-Body Control (WBC)')
dot.node('C', 'Desired Capture Point (DCM) Controller')
dot.node('D', 'State Estimation')
dot.node('E', 'Safety Layers')
dot.node('F', 'Simulation Support')
dot.node('G', 'Walking Actions and Tasks')
dot.node('H', 'Test Framework')
dot.node('I', 'ROS Integration')
dot.node('J', 'Plugin-based WBC')
dot.node('K', 'Abstraction Layers')
dot.node('L', 'Configuration Files')

# Connectors
dot.edge('A', 'B', label='controls')
dot.edge('B', 'C', label='uses')
dot.edge('B', 'D', label='receives feedback from')
dot.edge('B', 'E', label='ensures safety via')
dot.edge('A', 'F', label='supports simulation with')
dot.edge('A', 'G', label='supports various actions')
dot.edge('A', 'H', label='validated by')
dot.edge('A', 'I', label='integrates with')
dot.edge('B', 'J', label='dynamic loading via')
dot.edge('A', 'K', label='provides')
dot.edge('A', 'L', label='configured with')

# Styles
dot.attr('node', shape='rect', style='filled', color='lightgrey')
dot.attr('edge', arrowhead='open', arrowsize='1.5')

# Render to file
dot.render('talos_robot_locomotion_controller', format='png', cleanup=True)
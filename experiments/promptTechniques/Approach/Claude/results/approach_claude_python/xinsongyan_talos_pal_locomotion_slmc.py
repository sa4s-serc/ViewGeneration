import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(name='TALOS_Architecture', comment='TALOS Robot Locomotion Controller Architecture')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('wbc', 'Whole Body Control\n(WBC)', shape='box')
dot.node('dcm', 'DCM Controller', shape='box')
dot.node('state_est', 'State Estimation', shape='box')
dot.node('safety', 'Safety Layers', shape='box')
dot.node('sim', 'Simulation Support\n(Gazebo/PAL)', shape='box')
dot.node('walk', 'Walking Actions\nand Tasks', shape='box')
dot.node('test', 'Test Framework', shape='box')

# Create a subgraph for WBC implementations
with dot.subgraph(name='cluster_wbc') as c:
    c.attr(label='WBC Implementations')
    c.node('wbc_dyn', 'WbcWeightedDynamic\nCopTALOS')
    c.node('wbc_lower', 'WalkingWBCTalos\nLowerBodyTorsoHead')
    c.node('wbc_fixed', 'WalkingWBCTalos\nFixedUpperBody')

# Add edges to show relationships
dot.edge('dcm', 'wbc', 'Reference\nTrajectory')
dot.edge('state_est', 'wbc', 'Feedback')
dot.edge('wbc', 'walk', 'Control\nCommands')
dot.edge('safety', 'wbc', 'Constraints')
dot.edge('sim', 'state_est', 'Sensor Data')
dot.edge('test', 'walk', 'Validation')

# Connect WBC implementations
dot.edge('wbc', 'wbc_dyn', 'Plugin')
dot.edge('wbc', 'wbc_lower', 'Plugin')
dot.edge('wbc', 'wbc_fixed', 'Plugin')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr('node', fontsize='12')
dot.attr('edge', fontsize='10')

# Render the graph
dot.render('talos_architecture', format='png', cleanup=True)
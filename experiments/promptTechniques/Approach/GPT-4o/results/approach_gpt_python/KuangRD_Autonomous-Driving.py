from graphviz import Digraph

dot = Digraph(comment='Autonomous Driving System Architecture')

# Define styles
styles = {
    'graph': {
        'label': 'Autonomous Driving System Architecture',
        'fontsize': '16',
        'fontcolor': 'black',
        'bgcolor': 'white',
        'rankdir': 'LR',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'rect',
        'fontcolor': 'black',
        'color': 'black',
        'style': 'filled',
        'fillcolor': '#b3cde3',
    },
    'edges': {
        'style': 'solid',
        'color': 'black',
        'arrowhead': 'normal',
        'arrowsize': '1',
    }
}

# Apply styles
dot.attr(**styles['graph'])
dot.node_attr.update(styles['nodes'])
dot.edge_attr.update(styles['edges'])

# Define nodes
dot.node('Eigen', 'Eigen\nLinear Algebra')
dot.node('nlohmann::json', 'nlohmann::json\nJSON Handling')
dot.node('uWS', 'uWS\nWebSocket')
dot.node('BLAS/LAPACK', 'BLAS/LAPACK\nOptimized Libraries')
dot.node('TensorFlow/Keras', 'TensorFlow/Keras\nDeep Learning')
dot.node('ROS', 'ROS\nRobotics Framework')
dot.node('Traffic Light Classifier', 'Traffic Light Classifier\n(CNN Model)')
dot.node('Control Systems', 'Control Systems\n(PID Controller)')
dot.node('Docker', 'Docker\nDeployment')
dot.node('CMake', 'CMake\nBuild System')
dot.node('External Libraries', 'External Libraries\nIntegration')

# Define edges
dot.edge('Eigen', 'BLAS/LAPACK', 'Optimizes Performance')
dot.edge('nlohmann::json', 'ROS', 'JSON Communication')
dot.edge('uWS', 'ROS', 'WebSocket Communication')
dot.edge('TensorFlow/Keras', 'Traffic Light Classifier', 'Model Deployment')
dot.edge('ROS', 'Traffic Light Classifier', 'Node Integration')
dot.edge('ROS', 'Control Systems', 'Node Integration')
dot.edge('ROS', 'Docker', 'Containerized Nodes')
dot.edge('CMake', 'ROS', 'Build Management')
dot.edge('External Libraries', 'Eigen', 'Extended Functionality')
dot.edge('External Libraries', 'ROS', 'Enhanced Capabilities')

# Render the diagram
dot.render('architecture_diagram', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Hysia Video-to-Retail Platform Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('frontend', 'Frontend\n(React + Redux)')
dot.node('api', 'API Layer\n(Django + gRPC)')
dot.node('decode', 'Video Decoder\n(CPU/GPU)')
dot.node('ml', 'ML Models\n(Object/Face/Scene)')
dot.node('monitor', 'System Monitor')
dot.node('db', 'Storage\n(SQLite + Pickle)')

# Add subgraph for ML models
with dot.subgraph(name='cluster_ml') as ml_cluster:
    ml_cluster.attr(label='ML Processing')
    ml_cluster.node('object', 'Object Detection')
    ml_cluster.node('face', 'Face Recognition') 
    ml_cluster.node('scene', 'Scene Recognition')

# Add edges
dot.edge('frontend', 'api')
dot.edge('api', 'decode')
dot.edge('decode', 'ml')
dot.edge('ml', 'object')
dot.edge('ml', 'face')
dot.edge('ml', 'scene')
dot.edge('object', 'db')
dot.edge('face', 'db')
dot.edge('scene', 'db')
dot.edge('monitor', 'decode', 'monitors')
dot.edge('monitor', 'ml', 'monitors')
dot.edge('monitor', 'db', 'monitors')

# Save the diagram
dot.render('hysia_architecture', format='png', cleanup=True)
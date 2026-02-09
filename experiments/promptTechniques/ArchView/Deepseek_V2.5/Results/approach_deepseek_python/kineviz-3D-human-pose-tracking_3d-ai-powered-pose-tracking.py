import graphviz

dot = graphviz.Digraph(comment='3D Human Pose Tracking System Architecture')
dot.attr(rankdir='TB', size='8,8')

# Define nodes with styles
dot.node('webcam1', 'Webcam Client 1', shape='box', style='filled', fillcolor='lightblue')
dot.node('webcam2', 'Webcam Client 2', shape='box', style='filled', fillcolor='lightblue')
dot.node('server', 'Node.js Server\n(Express.js + Socket.IO)', shape='ellipse', style='filled', fillcolor='lightgreen')
dot.node('receiver', 'Receiver Client', shape='box', style='filled', fillcolor='lightcoral')
dot.node('graphxr', 'Kineviz GraphXR\nVisualization', shape='box', style='filled', fillcolor='plum')
dot.node('posenet', 'TensorFlow PoseNet/MoveNet', shape='box', style='filled', fillcolor='orange')

# Define edges with labels and styles
dot.edge('webcam1', 'server', label='skeleton data\n(Socket.IO)', style='dashed', color='blue')
dot.edge('webcam2', 'server', label='skeleton data\n(Socket.IO)', style='dashed', color='blue')
dot.edge('server', 'receiver', label='broadcast pose data\n(Socket.IO)', style='solid', color='red')
dot.edge('server', 'graphxr', label='pose data\n(WebSocket/API)', style='dotted', color='purple')
dot.edge('posenet', 'webcam1', label='2D pose estimation', style='solid', color='orange')
dot.edge('posenet', 'webcam2', label='2D pose estimation', style='solid', color='orange')

# Add a legend
with dot.subgraph(name='cluster_legend') as legend:
    legend.attr(label='Legend', style='dashed', color='gray')
    legend.node('legend_solid', 'Function Call / Data Processing', shape='plaintext')
    legend.node('legend_dashed', 'Real-time Data Stream (Socket.IO)', shape='plaintext')
    legend.node('legend_dotted', 'External Integration', shape='plaintext')

dot.render('architecture_diagram', format='png', cleanup=True)
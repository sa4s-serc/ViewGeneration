import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Graphrec Architecture View')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('android', 'Android Client\n(Mobile App)', shape='box')
dot.node('flask', 'Flask Server\n(Backend)', shape='box')
dot.node('cnn', 'CNN Model\n(TensorFlow)', shape='box')

# Add subgraph for Android components
with dot.subgraph(name='cluster_android') as android:
    android.attr(label='Android Components')
    android.node('main', 'MainActivity')
    android.node('camera', 'CameraActivity')
    android.node('result', 'ResultActivity')
    android.node('upload', 'ImageUploadTask')
    android.node('preview', 'CameraPreview')
    android.node('overlay', 'SurfaceOverlay')

# Add subgraph for Server components
with dot.subgraph(name='cluster_server') as server:
    server.attr(label='Server Components')
    server.node('server', 'server.py')
    server.node('classifier', 'graph_classifier.py')
    server.node('images', 'graph_images.py')
    server.node('generate', 'generate_data.py')

# Add edges between components
dot.edge('android', 'flask', 'HTTP POST\nImage Upload')
dot.edge('flask', 'android', 'Classification\nResult')
dot.edge('flask', 'cnn', 'Image\nClassification')
dot.edge('cnn', 'flask', 'Prediction')

# Add edges within Android components
dot.edge('main', 'camera')
dot.edge('camera', 'preview')
dot.edge('camera', 'overlay')
dot.edge('camera', 'result')
dot.edge('result', 'upload')
dot.edge('upload', 'android')

# Add edges within Server components
dot.edge('server', 'classifier')
dot.edge('classifier', 'images')
dot.edge('generate', 'images')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr('node', fontsize='12')
dot.attr('edge', fontsize='10')

# Save the diagram
dot.render('graphrec_architecture', format='png', cleanup=True)
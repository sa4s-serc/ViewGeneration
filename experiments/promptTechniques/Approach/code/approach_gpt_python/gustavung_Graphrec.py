from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Graphrec Architecture')

# Define client-server architecture
dot.node('Android App', 'Android App\n(Client)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Flask Server', 'Flask Server\n(Backend)', shape='rectangle', style='filled', fillcolor='lightgreen')

# Define core components
dot.node('MainActivity', 'MainActivity.java\n(Entry Point)', shape='rectangle')
dot.node('CameraActivity', 'CameraActivity.java\n(Camera)', shape='rectangle')
dot.node('ResultActivity', 'ResultActivity.java\n(Result Display)', shape='rectangle')
dot.node('ImageUploadTask', 'ImageUploadTask.java\n(AsyncTask)', shape='rectangle')

dot.node('server.py', 'server.py\n(Main Flask App)', shape='rectangle')
dot.node('graph_classifier.py', 'graph_classifier.py\n(CNN Model)', shape='rectangle')
dot.node('graph_images.py', 'graph_images.py\n(Image Processing)', shape='rectangle')
dot.node('generate_data.py', 'generate_data.py\n(Data Generation)', shape='rectangle')
dot.node('cn.py', 'cn.py\n(CNN Operations)', shape='rectangle')

# Define connections between components
dot.edge('Android App', 'Flask Server', label='HTTP POST\n(Image Upload)', arrowhead='normal')
dot.edge('MainActivity', 'CameraActivity', label='Launch Camera', arrowhead='normal')
dot.edge('CameraActivity', 'ImageUploadTask', label='Start Upload Task', arrowhead='normal')
dot.edge('ImageUploadTask', 'Flask Server', label='Send Image', arrowhead='normal')
dot.edge('Flask Server', 'ResultActivity', label='Return Result', arrowhead='normal')
dot.edge('server.py', 'graph_classifier.py', label='Invoke Classification', arrowhead='normal')
dot.edge('graph_classifier.py', 'graph_images.py', label='Process Images', arrowhead='normal')
dot.edge('graph_classifier.py', 'cn.py', label='Train/Evaluate CNN', arrowhead='normal')
dot.edge('generate_data.py', 'graph_classifier.py', label='Provide Data', arrowhead='normal')

# Render the diagram
dot.render('graphrec_architecture', format='png', cleanup=True)
from graphviz import Digraph

dot = Digraph(comment='Trainspotting Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('camera', 'Video Camera\n(Raspberry Pi)')
dot.node('video_sensor', 'Video Sensor\n(Background Subtraction)')
dot.node('video_detector', 'Video Detector\n(Motion Analysis)')
dot.node('classifier', 'TensorFlow Classifier')
dot.node('data_store', 'Data Storage\n(Deques & DataFrames)')
dot.node('visualizer', 'Data Visualizer')

# Add subgraph for ROI processing
with dot.subgraph(name='cluster_roi') as roi:
    roi.attr(label='ROI Processing')
    roi.node('roi_extract', 'ROI Extraction')
    roi.node('motion_detect', 'Motion Detection')
    roi.node('direction_detect', 'Direction Detection')

# Add connections
dot.edge('camera', 'video_sensor', 'Video Frames')
dot.edge('video_sensor', 'roi_extract', 'Processed Frames')
dot.edge('roi_extract', 'motion_detect', 'ROI Data')
dot.edge('motion_detect', 'direction_detect', 'Motion Events')
dot.edge('video_sensor', 'video_detector', 'Frame Data')
dot.edge('video_detector', 'classifier', 'Objects')
dot.edge('classifier', 'data_store', 'Classifications')
dot.edge('direction_detect', 'data_store', 'Direction Data')
dot.edge('data_store', 'visualizer', 'Analysis Data')

# Set graph attributes
dot.attr(label='Trainspotting System Architecture', labelloc='t')
dot.attr(fontsize='20')

# Save the diagram
dot.render('trainspotting_architecture', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Trainspotting Architecture')

# Define nodes for main components
dot.node('RPi', 'Raspberry Pi', shape='rect', style='filled', fillcolor='lightblue')
dot.node('VCam', 'Video_Camera', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('VSen', 'Video_Sensor', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('VDet', 'Video_Detector', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('TensorFlow', 'TensorFlow Model', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('DataStore', 'Data Storage', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('Vis', 'Data Visualization', shape='rect', style='filled', fillcolor='lightpink')

# Add edges for data flow
dot.edge('RPi', 'VCam', 'captures video', style='dashed')
dot.edge('VCam', 'VSen', 'produces frames')
dot.edge('VSen', 'VDet', 'processes frames')
dot.edge('VDet', 'TensorFlow', 'classifies objects')
dot.edge('VDet', 'DataStore', 'stores events')
dot.edge('DataStore', 'Vis', 'visualizes data')

# Add edges for control flow
dot.edge('VDet', 'VCam', 'dynamic adjustments', style='dotted')
dot.edge('VDet', 'VSen', 'motion detection triggers', style='dotted')

# Render the graph to a file
dot.render('trainspotting_architecture', format='png', cleanup=True)
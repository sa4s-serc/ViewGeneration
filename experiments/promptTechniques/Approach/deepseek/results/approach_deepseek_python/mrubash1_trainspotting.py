import graphviz

# Create a new directed graph
dot = graphviz.Digraph('Trainspotting_Architecture', comment='Trainspotting Repository Architecture')
dot.attr(rankdir='TB', size='8,10')

# Define nodes with styles
dot.node('RPi_Camera', 'Raspberry Pi Camera', shape='box', style='filled', fillcolor='lightblue')
dot.node('Video_Camera', 'Video_Camera\n(Producer)', shape='box', style='filled', fillcolor='lightcoral')
dot.node('Input_Deque', 'Input Deque\n(Data Pipeline)', shape='cylinder', style='filled', fillcolor='lightyellow')
dot.node('Video_Sensor', 'Video_Sensor\n(Consumer)', shape='box', style='filled', fillcolor='lightgreen')
dot.node('Mask', 'Mask\n(Strategy Pattern)', shape='box', style='filled', fillcolor='lightpink')
dot.node('Video_Detector', 'Video_Detector\n(Consumer)', shape='box', style='filled', fillcolor='lightcyan')
dot.node('TensorFlow', 'TensorFlow Model\n(Classification)', shape='box', style='filled', fillcolor='orange')
dot.node('Data_Storage', 'Data Storage\n(Deques & DataFrames)', shape='cylinder', style='filled', fillcolor='lightyellow')
dot.node('Visualization', 'Data Visualization\n(Plots & Images)', shape='box', style='filled', fillcolor='plum')
dot.node('Cloud_Services', 'Cloud Services\n(Potential)', shape='box', style='filled', fillcolor='wheat')

# Define edges to represent data flow and interactions
dot.edge('RPi_Camera', 'Video_Camera', label='Real-time Video', style='solid')
dot.edge('Video_Camera', 'Input_Deque', label='Frames', style='solid')
dot.edge('Input_Deque', 'Video_Sensor', label='Frames', style='solid')
dot.edge('Video_Sensor', 'Mask', label='Background Subtraction', style='dashed')
dot.edge('Mask', 'Video_Sensor', label='Processed Frames', style='dashed')
dot.edge('Video_Sensor', 'Video_Detector', label='Motion Data', style='solid')
dot.edge('Video_Detector', 'TensorFlow', label='ROI for Classification', style='solid')
dot.edge('TensorFlow', 'Video_Detector', label='Classification Results', style='solid')
dot.edge('Video_Detector', 'Data_Storage', label='Detection Events', style='solid')
dot.edge('Data_Storage', 'Visualization', label='Data for Plots', style='solid')
dot.edge('Data_Storage', 'Cloud_Services', label='Potential Upload', style='dotted')

# Add a subgraph for parallel processing (threading)
with dot.subgraph(name='cluster_parallel') as c:
    c.attr(label='Parallel Processing (Threading)', style='dashed', color='blue')
    c.node('Video_Camera')
    c.node('Video_Sensor')
    c.node('Video_Detector')

# Add a subgraph for event-driven operation
with dot.subgraph(name='cluster_event') as e:
    e.attr(label='Event-Driven Operation', style='dashed', color='green')
    e.node('Video_Detector')
    e.node('TensorFlow')

# Render the diagram
dot.render(format='png', cleanup=True)
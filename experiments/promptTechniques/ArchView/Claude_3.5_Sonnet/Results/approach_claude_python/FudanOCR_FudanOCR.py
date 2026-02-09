from graphviz import Digraph

dot = Digraph('FudanOCR Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('detection', 'Text Detection\n(EAST, PSENet, TextSnake)')
dot.node('recognition', 'Text Recognition\n(CRNN, MORAN, GRCNN)')
dot.node('sr', 'Super Resolution\n(DocumentSRModel)')
dot.node('data', 'Data Handling\n(Loaders, Augmentation)')
dot.node('train', 'Training Engine')
dot.node('post', 'Post Processing\n(NMS, Filtering)')
dot.node('config', 'Configuration\n(YAML)')
dot.node('custom', 'Custom Operations\n(ROIAlign, RROIAlign)')

# Add edges
dot.edge('data', 'detection', 'Dataset Input')
dot.edge('data', 'recognition', 'Dataset Input')
dot.edge('data', 'sr', 'Dataset Input')
dot.edge('detection', 'post', 'Detection Results')
dot.edge('post', 'recognition', 'Filtered Regions')
dot.edge('sr', 'detection', 'Enhanced Images')
dot.edge('config', 'train', 'Parameters')
dot.edge('train', 'detection', 'Training')
dot.edge('train', 'recognition', 'Training')
dot.edge('train', 'sr', 'Training')
dot.edge('custom', 'detection', 'Custom Ops')
dot.edge('custom', 'recognition', 'Custom Ops')

# Print the dot source
print(dot.source)

# Render the diagram
dot.render('fudan_ocr_architecture', view=True, format='png')
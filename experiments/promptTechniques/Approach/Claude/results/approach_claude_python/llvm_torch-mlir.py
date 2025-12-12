import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Torch-MLIR Architecture')
dot.attr(rankdir='TB')

# Set global node and edge attributes
dot.attr('node', shape='rectangle', style='filled,rounded', fillcolor='lightgray')
dot.attr('edge', color='gray50', fontsize='10')

# Frontend Layer
with dot.subgraph(name='cluster_0') as frontend:
    frontend.attr(label='Frontend Layer', style='rounded', color='blue')
    frontend.node('ltc', 'Tracing-based (LTC)\nTraining Support')
    frontend.node('torchscript', 'TorchScript & FX\nGraph Importers')

# Core Dialects Layer
with dot.subgraph(name='cluster_1') as dialects:
    dialects.attr(label='Core Dialects', style='rounded', color='darkgreen')
    dialects.node('torch', 'Torch Dialect\n(TableGen Defined)')
    dialects.node('tmtensor', 'TMTensor Dialect')
    dialects.node('conv', 'TorchConversion\nDialect')

# Transformation Layer
with dot.subgraph(name='cluster_2') as transforms:
    transforms.attr(label='Transformation Passes', style='rounded', color='red')
    transforms.node('shape', 'Shape/Dtype\nCalculations')
    transforms.node('calling', 'Calling\nConventions')
    transforms.node('global', 'Object Graph\nGlobalization')
    transforms.node('contract', 'Backend Contract\nLowering')

# Backend Layer
with dot.subgraph(name='cluster_3') as backend:
    backend.attr(label='Backend Targets', style='rounded', color='purple')
    backend.node('linalg', 'Linalg-on-Tensors')
    backend.node('tosa', 'TOSA')
    backend.node('stablehlo', 'StableHLO')
    backend.node('onnx', 'ONNX')

# Add edges between components
dot.edge('ltc', 'torch')
dot.edge('torchscript', 'torch')
dot.edge('torch', 'shape')
dot.edge('torch', 'tmtensor')
dot.edge('tmtensor', 'conv')
dot.edge('shape', 'calling')
dot.edge('calling', 'global')
dot.edge('global', 'contract')
dot.edge('conv', 'contract')
dot.edge('contract', 'linalg')
dot.edge('contract', 'tosa')
dot.edge('contract', 'stablehlo')
dot.edge('contract', 'onnx')

# Save the diagram
dot.render('torch_mlir_architecture', format='png', cleanup=True)
from graphviz import Digraph

def create_torch_mlir_architecture_diagram():
    dot = Digraph(comment='Torch-MLIR Architecture')

    # Add nodes for key components and dialects
    dot.node('Torch', 'Torch Dialect')
    dot.node('TMTensor', 'TMTensor Dialect')
    dot.node('TorchConversion', 'TorchConversion Dialect')
    dot.node('LTC', 'Tracing-based (LTC)')
    dot.node('TorchScriptFX', 'TorchScript & FX Graph Importers')
    dot.node('BackendContract', 'Backend Contract')
    dot.node('PassDriven', 'Pass-driven Backend Conversion')
    dot.node('Linalg', 'Linalg-on-Tensors')
    dot.node('TOSA', 'TOSA')
    dot.node('StableHLO', 'StableHLO')
    dot.node('ONNX', 'ONNX Importer')
    dot.node('LazyTensor', 'Lazy Tensor Core')

    # Add edges to represent communication and transformation flows
    dot.edge('Torch', 'TorchConversion', label='Conversion')
    dot.edge('TorchConversion', 'TMTensor', label='Intermediate Transformation')
    dot.edge('TorchConversion', 'Linalg', label='Lowering')
    dot.edge('TorchConversion', 'TOSA', label='Lowering')
    dot.edge('TorchConversion', 'StableHLO', label='Lowering')
    dot.edge('Torch', 'BackendContract', label='Defines Contract')
    dot.edge('LTC', 'Torch', label='Tracing-based Frontend')
    dot.edge('TorchScriptFX', 'Torch', label='Import and Lowering')
    dot.edge('BackendContract', 'PassDriven', label='Defines')
    dot.edge('PassDriven', 'Linalg', label='Transform')
    dot.edge('PassDriven', 'TOSA', label='Transform')
    dot.edge('PassDriven', 'StableHLO', label='Transform')
    dot.edge('ONNX', 'Torch', label='Import')
    dot.edge('LazyTensor', 'Torch', label='Optimization')

    # Add styling for clarity
    dot.attr('node', shape='rect')
    dot.attr('edge', arrowsize='0.7')

    # Render the diagram
    dot.render('torch_mlir_architecture_diagram', format='png', cleanup=True)

create_torch_mlir_architecture_diagram()
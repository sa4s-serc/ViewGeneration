from diagrams import Diagram
from diagrams.programming.language import Python
from diagrams.programming.framework import Django
from diagrams.generic.blank import Blank
from diagrams.custom import Custom

with Diagram("Torch-MLIR Architecture", show=False, direction="TB"):
    pytorch_frontends = Custom("PyTorch Frontends\n(Tracing, TorchScript, FX)", "./pytorch.png")
    
    torch_dialect = Custom("Torch Dialect\n(ATen ops, value semantics)", "./mlir.png")
    torch_conversion = Custom("TorchConversion Dialect\n(Type conversions)", "./mlir.png")
    tm_tensor = Custom("TMTensor Dialect\n(Intermediate representation)", "./mlir.png")
    
    transformation_passes = Custom("Transformation Passes\n(Shape reification, Globalize, Scalarize)", "./compiler.png")
    
    backend_contract = Custom("Backend Contract\n(Value semantics, known shapes/dtypes)", "./contract.png")
    
    backends = Custom("Backend Targets\n(Linalg, TOSA, StableHLO, ONNX, LTC)", "./target.png")
    
    code_generation = Custom("Code Generation\n(TableGen, Python bindings, C-API)", "./code.png")
    
    testing = Custom("Testing Framework\n(E2E tests, LIT, Unit tests)", "./testing.png")
    
    pytorch_frontends >> torch_dialect
    torch_dialect >> transformation_passes
    transformation_passes >> backend_contract
    backend_contract >> backends
    backends >> code_generation
    torch_dialect >> torch_conversion
    torch_conversion >> tm_tensor
    tm_tensor >> transformation_passes
    code_generation >> testing
from diagrams import Diagram
from diagrams.programming.language import Cpp
from diagrams.generic.blank import Blank
from diagrams.custom import Custom

with Diagram("Eigen Library Architecture", show=False, direction="TB"):
    # Core components
    expression_templates = Custom("Expression Templates", "./box.png")
    templates_metaprogramming = Custom("Templates & Metaprogramming", "./box.png")
    simd_vectorization = Custom("SIMD Vectorization", "./box.png")
    memory_management = Custom("Memory Management", "./box.png")
    
    # Main modules
    core_module = Cpp("Core Module")
    dense_linear_algebra = Cpp("Dense Linear Algebra")
    sparse_linear_algebra = Cpp("Sparse Linear Algebra")
    decomposition_algorithms = Cpp("Decomposition Algorithms")
    eigenvalue_solvers = Cpp("Eigenvalue Solvers")
    iterative_solvers = Cpp("Iterative Solvers")
    geometry_module = Cpp("Geometry Module")
    
    # Unsupported module components
    unsupported_module = Cpp("Unsupported Module")
    tensor_operations = Cpp("Tensor Operations")
    matrix_functions = Cpp("Matrix Functions")
    nonlinear_optimization = Cpp("NonLinear Optimization")
    
    # External integrations
    blas_lapack = Custom("BLAS/LAPACK Integration", "./box.png")
    testing_framework = Custom("Testing Framework", "./box.png")
    documentation = Custom("Documentation", "./box.png")
    
    # Architectural patterns
    expression_templates_pattern = Custom("Expression Templates Pattern", "./box.png")
    traits_pattern = Custom("Traits Pattern", "./box.png")
    policy_based_design = Custom("Policy-Based Design", "./box.png")
    strategy_pattern = Custom("Strategy Pattern", "./box.png")
    bridge_pattern = Custom("Bridge Pattern", "./box.png")
    
    # Connect core architectural components
    expression_templates >> templates_metaprogramming
    templates_metaprogramming >> simd_vectorization
    simd_vectorization >> memory_management
    
    # Connect core components to main modules
    [expression_templates, templates_metaprogramming, simd_vectorization, memory_management] >> core_module
    core_module >> [dense_linear_algebra, sparse_linear_algebra, decomposition_algorithms, eigenvalue_solvers, iterative_solvers, geometry_module]
    
    # Connect unsupported module
    core_module >> unsupported_module
    unsupported_module >> [tensor_operations, matrix_functions, nonlinear_optimization]
    
    # Connect external integrations
    core_module >> blas_lapack
    core_module >> testing_framework
    core_module >> documentation
    
    # Connect design patterns
    expression_templates_pattern >> expression_templates
    traits_pattern >> templates_metaprogramming
    policy_based_design >> templates_metaprogramming
    strategy_pattern >> iterative_solvers
    bridge_pattern >> blas_lapack
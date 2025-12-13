from graphviz import Digraph

dot = Digraph(comment='Eigen Library Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Core components
dot.node('core', 'Core Module\n- Dense/Sparse Linear Algebra\n- Matrix/Vector Operations')
dot.node('expr', 'Expression Templates\n- Deferred Evaluation\n- Compile-time Optimization')
dot.node('mem', 'Memory Management\n- Aligned Allocation\n- SIMD Optimization')

# Modules
dot.node('decomp', 'Decomposition\n- LU, Cholesky\n- QR, SVD')
dot.node('eigen', 'Eigensolvers\n- EigenSolver\n- SelfAdjointSolver') 
dot.node('sparse', 'Sparse Module\n- Sparse Matrices\n- Iterative Solvers')
dot.node('geom', 'Geometry Module\n- Transforms\n- Quaternions')

# Integration components
dot.node('blas', 'BLAS/LAPACK\nIntegration')
dot.node('simd', 'SIMD Vectorization\n- SSE, AVX, NEON')

# Add edges
dot.edge('expr', 'core')
dot.edge('mem', 'core')
dot.edge('core', 'decomp')
dot.edge('core', 'eigen')
dot.edge('core', 'sparse')
dot.edge('core', 'geom')
dot.edge('blas', 'core')
dot.edge('simd', 'core')
dot.edge('sparse', 'eigen', 'uses')

# Add subgraph for external integration
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='External Integration')
    c.node('mkl', 'Intel MKL')
    c.node('cuda', 'CUDA')
    c.edge('mkl', 'blas')
    c.edge('cuda', 'blas')

dot.render('eigen_architecture', view=True, format='png')
from graphviz import Digraph

# Create a graph object
dot = Digraph(comment='Eigen Library Architecture')

# Set graph attributes
dot.attr(rankdir='LR', size='10,8')
dot.attr('node', shape='rectangle')

# Add core functionalities
dot.node('1', 'Dense & Sparse Linear Algebra')
dot.node('2', 'Decomposition Algorithms')
dot.node('3', 'Eigenvalue Solvers')
dot.node('4', 'Iterative Linear Solvers')
dot.node('5', 'Geometry')
dot.node('6', 'Tensor Operations')

# Add architecture components
dot.node('7', 'Expression Templates')
dot.node('8', 'Templates & Metaprogramming')
dot.node('9', 'Memory Management')
dot.node('10', 'SIMD Vectorization')
dot.node('11', 'Modular Design')
dot.node('12', 'BLAS/LAPACK Integration')
dot.node('13', 'Plugin System')

# Add key design patterns
dot.node('14', 'Expression Templates Pattern')
dot.node('15', 'Traits')
dot.node('16', 'Policy-Based Design')
dot.node('17', 'Strategy Pattern')
dot.node('18', 'Bridge Pattern')

# Add testing and documentation
dot.node('19', 'Testing and Documentation')
dot.node('20', 'Unsupported Module Highlights')

# Connect core functionalities to architecture components
dot.edges([('1', '7'), ('1', '8'), ('2', '7'), ('3', '7'), ('4', '7'),
           ('5', '7'), ('6', '7')])

# Connect architecture components
dot.edges([('7', '8'), ('8', '9'), ('9', '10'), ('10', '11'),
           ('11', '12'), ('12', '13')])

# Connect key design patterns
dot.edges([('14', '7'), ('15', '8'), ('16', '8'), ('17', '4'), ('18', '12')])

# Connect testing and documentation
dot.edge('19', '20')

# Render and view the diagram
dot.render('eigen_architecture_diagram', format='png', cleanup=True)
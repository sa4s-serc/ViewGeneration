import graphviz

# Create a new directed graph
dot = graphviz.Digraph('FluxSurfer Architecture', 
    graph_attr={
        'rankdir': 'TB',
        'splines': 'ortho',
        'overlap': 'false',
        'fontname': 'Arial',
        'bgcolor': 'white'
    }
)

# Define node styles
dot.attr('node', 
    shape='box',
    style='rounded,filled',
    fillcolor='lightblue',
    fontname='Arial',
    margin='0.3,0.1'
)

# Core Components
dot.node('quantum_system', 'QuantumSystem\nGraph Structure\n(States & Transitions)')
dot.node('experiment', 'Experiment Class\nParallel Processing\nMetadata Management')

# Solvers Cluster
with dot.subgraph(name='cluster_solvers') as c:
    c.attr(label='Solvers', style='rounded', bgcolor='lightgrey')
    c.node('ode_solvers', 'ODE Solvers\nAdaptive/Fixed Step')
    c.node('monte_carlo', 'MonteCarloWanderer\nDirect Graph Exploration')
    c.node('solver_base', 'Solver\n(Abstract Base Class)')

# Storage Cluster
with dot.subgraph(name='cluster_storage') as c:
    c.attr(label='Data Storage', style='rounded', bgcolor='lightyellow')
    c.node('graphml', '.graphml Files\n(Graph Structure & Data)')
    c.node('metadata_json', 'METADATA.json\n(Parameters & Description)')
    c.node('metadata_csv', 'METADATA.csv\n(Measurement Data)')

# Utilities Cluster
with dot.subgraph(name='cluster_utils') as c:
    c.attr(label='Utilities', style='rounded', bgcolor='lightgreen')
    c.node('binary_utils', 'Binary Number Utils')
    c.node('xml_parser', 'XML File Parser')

# Define relationships
dot.edge('quantum_system', 'solver_base', 'provides data')
dot.edge('solver_base', 'ode_solvers', 'implements')
dot.edge('solver_base', 'monte_carlo', 'implements')
dot.edge('experiment', 'quantum_system', 'manages')
dot.edge('experiment', 'graphml', 'writes')
dot.edge('experiment', 'metadata_json', 'writes')
dot.edge('experiment', 'metadata_csv', 'writes')
dot.edge('quantum_system', 'binary_utils', 'uses')
dot.edge('graphml', 'xml_parser', 'parsed by')

# Save the diagram
dot.render('fluxsurfer_architecture', format='png', cleanup=True)
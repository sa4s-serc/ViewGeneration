from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='FluxSurfer Architecture')

# Add nodes for each key component
dot.node('QS', 'QuantumSystem Class', shape='rectangle')
dot.node('ODE', 'ODE Solvers', shape='rectangle')
dot.node('MCW', 'MonteCarloWanderer', shape='rectangle')
dot.node('EXP', 'Experiment Class', shape='rectangle')
dot.node('PAR', 'Parallelization', shape='rectangle')
dot.node('DS', 'Data Storage', shape='rectangle')
dot.node('UTIL', 'Utilities', shape='rectangle')

# Add edges to represent relationships and control flow
dot.edge('QS', 'ODE', label='uses')
dot.edge('QS', 'MCW', label='uses')
dot.edge('EXP', 'PAR', label='manages')
dot.edge('EXP', 'DS', label='stores data')
dot.edge('EXP', 'QS', label='coordinates')
dot.edge('PAR', 'EXP', label='executes')
dot.edge('DS', 'EXP', label='saves')
dot.edge('UTIL', 'DS', label='enhances')
dot.edge('UTIL', 'QS', label='supports')

# Render and display the graph
dot.render('flux_surfer_architecture', format='png', cleanup=True)
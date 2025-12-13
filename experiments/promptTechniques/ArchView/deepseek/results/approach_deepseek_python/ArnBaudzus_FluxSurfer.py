from graphviz import Digraph

dot = Digraph(comment='FluxSurfer Architecture', format='png')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_core') as c:
    c.attr(label='Core Components', style='filled', color='lightgrey')
    c.node('QuantumSystem', 'QuantumSystem\n- Graph structure\n- State/Edge management\n- Data storage (.graphml)', shape='box', style='filled', color='lightblue')
    c.node('State', 'State\n- Quantum state representation', shape='ellipse')
    c.node('Edge', 'Edge\n- Transition probabilities', shape='ellipse')

with dot.subgraph(name='cluster_solvers') as s:
    s.attr(label='Solvers', style='filled', color='lightyellow')
    s.node('Solver', 'Solver\n(Abstract Base Class)', shape='box', style='dashed')
    s.node('ODESolvers', 'ODE Solvers\n- EulerForward\n- RichardsonSolver', shape='box')
    s.node('SingleStepScheme', 'SingleStepScheme\n(Abstract Base Class)', shape='box', style='dashed')
    s.node('MonteCarloWanderer', 'MonteCarloWanderer\n- Graph exploration', shape='box')

with dot.subgraph(name='cluster_experiment') as e:
    e.attr(label='Experiment Management', style='filled', color='lightgreen')
    e.node('Experiment', 'Experiment\n- Parallel processing\n- Metadata storage\n- Measurement coordination', shape='box')
    e.node('WorkSource', 'WorkSource\n(Shared Queue)', shape='box')
    e.node('DataSet', 'DataSet', shape='box')

with dot.subgraph(name='cluster_tools') as t:
    t.attr(label='Tools & Utilities', style='filled', color='lightpink')
    t.node('FileUtility', 'fileUtility.py\n- GraphML parsing', shape='box')
    t.node('Quantities', 'quantities.py\n- Physical calculations', shape='box')
    t.node('PlotChargeCurve', 'plotChargeCurve.py\n- Visualization', shape='box')
    t.node('BinaryUtility', 'binaryNumberUtility.py\n- State ID handling', shape='box')

dot.edge('QuantumSystem', 'State', label='contains')
dot.edge('QuantumSystem', 'Edge', label='contains')
dot.edge('Solver', 'ODESolvers', label='inherits')
dot.edge('Solver', 'MonteCarloWanderer', label='inherits')
dot.edge('SingleStepScheme', 'ODESolvers', label='strategy')
dot.edge('Experiment', 'QuantumSystem', label='manages')
dot.edge('Experiment', 'Solver', label='executes')
dot.edge('Experiment', 'WorkSource', label='uses')
dot.edge('Experiment', 'DataSet', label='stores')
dot.edge('FileUtility', 'QuantumSystem', label='parses')
dot.edge('Quantities', 'QuantumSystem', label='analyzes')
dot.edge('PlotChargeCurve', 'DataSet', label='visualizes')
dot.edge('BinaryUtility', 'State', label='processes')

dot.render('fluxsurfer_architecture', cleanup=True)
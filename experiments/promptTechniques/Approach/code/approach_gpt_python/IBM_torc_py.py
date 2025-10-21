from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='IBM_torc_py Architecture')

# Define nodes for core components
dot.node('TM', 'Task Management', shape='rectangle', style='filled', color='lightblue')
dot.node('ASC', 'Application Setup & Control', shape='rectangle', style='filled', color='lightgreen')
dot.node('LB', 'Load Balancing', shape='rectangle', style='filled', color='lightcoral')
dot.node('SPMD', 'SPMD Support', shape='rectangle', style='filled', color='lightyellow')
dot.node('CB', 'Callbacks', shape='rectangle', style='filled', color='lightgrey')
dot.node('CM', 'Context Manager', shape='rectangle', style='filled', color='lightpink')

# Define nodes for architecture
dot.node('HM', 'Hybrid MPI & Multithreading', shape='ellipse', style='filled', color='orange')
dot.node('MW', 'Master-Worker Model', shape='ellipse', style='filled', color='lightblue')
dot.node('TQ', 'Task Queue', shape='ellipse', style='filled', color='lightgreen')
dot.node('ST', 'Server Thread', shape='ellipse', style='filled', color='lightcoral')
dot.node('AO', 'Asynchronous Operations', shape='ellipse', style='filled', color='lightyellow')

# Define relationships (edges)
dot.edge('TM', 'ASC', label='manages')
dot.edge('ASC', 'LB', label='distributes')
dot.edge('LB', 'SPMD', label='enables')
dot.edge('SPMD', 'CB', label='supports')
dot.edge('CB', 'CM', label='wraps')
dot.edge('CM', 'TM', label='submits')

# Define architecture relationships
dot.edge('HM', 'MW', label='employs')
dot.edge('MW', 'TQ', label='operates')
dot.edge('TQ', 'ST', label='manages')
dot.edge('ST', 'AO', label='facilitates')

# Render the graph to a file
dot.render('ibm_torc_py_architecture', format='png', cleanup=True)
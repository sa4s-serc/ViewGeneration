import graphviz

# Create a new directed graph
g = graphviz.Digraph('IBM_torc_py_Architecture')
g.attr(rankdir='TB')

# Define node attributes
g.attr('node', shape='rectangle', style='rounded', fontname='Arial', fontsize='10')

# Add main component clusters
with g.subgraph(name='cluster_0') as c:
    c.attr(label='Core Components', style='rounded', color='lightblue')
    c.node('task_mgmt', 'Task Management\n(submit, map, wait, as_completed)', color='blue')
    c.node('app_setup', 'Application Setup & Control\n(start, init, launch, shutdown)', color='blue')
    c.node('load_bal', 'Load Balancing\n(round-robin, task stealing)', color='blue')

with g.subgraph(name='cluster_1') as c:
    c.attr(label='Runtime System', style='rounded', color='lightgreen')
    c.node('mpi', 'MPI Communication\n(mpi4py)', color='green')
    c.node('threads', 'Threading\nManagement', color='green')
    c.node('queue', 'Task Queue\n(torc_q)', color='green')
    c.node('server', 'Server Thread\n(torc_server_thread)', color='green')

with g.subgraph(name='cluster_2') as c:
    c.attr(label='Additional Features', style='rounded', color='lightpink')
    c.node('spmd', 'SPMD Support', color='red')
    c.node('callbacks', 'Callbacks', color='red')
    c.node('executor', 'TorcPoolExecutor', color='red')

# Add edges
g.edge('app_setup', 'task_mgmt')
g.edge('app_setup', 'load_bal')
g.edge('task_mgmt', 'queue')
g.edge('queue', 'server')
g.edge('server', 'mpi')
g.edge('load_bal', 'server')
g.edge('task_mgmt', 'callbacks')
g.edge('spmd', 'mpi')
g.edge('executor', 'threads')
g.edge('threads', 'queue')
g.edge('mpi', 'load_bal')

# Save the graph
g.render('ibm_torc_architecture', format='png', cleanup=True)
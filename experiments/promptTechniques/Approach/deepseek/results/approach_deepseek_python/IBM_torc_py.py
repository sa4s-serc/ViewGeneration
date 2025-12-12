import graphviz

dot = graphviz.Digraph(comment='IBM_torc_py Architecture')
dot.attr(rankdir='TB', size='12,10')

# Main components
with dot.subgraph(name='cluster_master') as master:
    master.attr(label='Master Process (Rank 0)', style='filled', color='lightblue')
    master.node('app_task', 'Application Task', shape='ellipse')
    master.node('torc_api', 'TORC API\n(submit, map, wait, etc.)', shape='box')
    master.node('master_queue', 'Task Queue', shape='folder')

with dot.subgraph(name='cluster_worker') as worker:
    worker.attr(label='Worker Processes', style='filled', color='lightgreen')
    worker.node('worker_threads', 'Worker Threads', shape='box')
    worker.node('worker_queue', 'Task Queue', shape='folder')
    worker.node('server_thread', 'Server Thread', shape='box')

# Additional components
dot.node('mpi', 'MPI (mpi4py)', shape='hexagon')
dot.node('threading', 'Threading Module', shape='hexagon')
dot.node('torc_pool', 'TorcPoolExecutor', shape='box')
dot.node('spmd', 'SPMD Support', shape='box')
dot.node('callbacks', 'Callbacks', shape='box')

# Connections
dot.edge('app_task', 'torc_api')
dot.edge('torc_api', 'master_queue')
dot.edge('master_queue', 'mpi', label='task distribution')
dot.edge('mpi', 'worker_queue')
dot.edge('worker_queue', 'worker_threads')
dot.edge('worker_threads', 'server_thread')
dot.edge('server_thread', 'mpi', label='results/task stealing')
dot.edge('mpi', 'master_queue', label='results')
dot.edge('torc_pool', 'worker_threads', style='dashed')
dot.edge('spmd', 'mpi', style='dashed')
dot.edge('worker_threads', 'callbacks', style='dashed', label='on completion')
dot.edge('threading', 'worker_threads', style='dashed')

# Load balancing annotation
dot.node('lb', 'Load Balancing:\n- Round-robin\n- Task stealing', shape='note')
dot.edge('lb', 'mpi', style='invis')

# Render the diagram
dot.render('ibm_torc_py_architecture', format='png', cleanup=True)
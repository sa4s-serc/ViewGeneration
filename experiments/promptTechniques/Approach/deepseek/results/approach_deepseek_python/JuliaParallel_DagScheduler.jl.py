import graphviz

dot = graphviz.Digraph(comment='DagScheduler Architecture')
dot.attr(rankdir='TB', size='8,10')

# Main components
with dot.subgraph(name='cluster_main') as c:
    c.attr(label='DagScheduler.jl', style='filled', color='lightgrey')
    c.node('rundag', 'rundag Function\n(DAG Execution)', shape='ellipse', style='filled', color='lightblue')
    c.node('scheduler', 'Scheduler\n(Task Prioritization, DAG Decomposition)', shape='box', style='filled', color='lightcoral')
    c.node('engine', 'Execution Engine\n(Task Coordination, Failure Handling)', shape='box', style='filled', color='lightgreen')
    c.node('queue', 'Execution Queue\n(Task Assignment)', shape='box', style='filled', color='lightyellow')

# Metadata stores
with dot.subgraph(name='cluster_meta') as c:
    c.attr(label='Metadata Stores', style='filled', color='lightcyan')
    c.node('shmem', 'ShmemMetaStore\n(Shared Memory)', shape='cylinder', style='filled', color='white')
    c.node('simple', 'SimpleMetaStore\n(Julia Messaging)', shape='cylinder', style='filled', color='white')
    c.node('fdb', 'FDBMetaStore\n(FoundationDB)', shape='cylinder', style='filled', color='white')

# Tiered architecture
with dot.subgraph(name='cluster_tiered') as c:
    c.attr(label='Tiered Architecture', style='filled', color='lightpink')
    c.node('node', 'Node\n(Physical Machine)', shape='box3d', style='filled', color='white')
    c.node('broker', 'Broker\n(Process Coordination)', shape='box', style='filled', color='lightgoldenrod')
    c.node('executor', 'Executor\n(Task Execution)', shape='box', style='filled', color='lightsteelblue')

# External integrations
dot.node('dagger', 'Dagger.jl\n(Plugin Integration)', shape='hexagon', style='filled', color='plum')
dot.node('remotemonitor', 'RemoteMonitor\n(Remote Monitoring)', shape='parallelogram', style='filled', color='wheat')
dot.node('foundationdb', 'FoundationDB\n(Persistent Storage)', shape='cylinder', style='filled', color='tan')

# Data flow connections
dot.edge('rundag', 'scheduler', label='DAG Input')
dot.edge('scheduler', 'engine', label='Scheduled Tasks')
dot.edge('engine', 'queue', label='Task Assignment')
dot.edge('queue', 'executor', label='Task Execution')
dot.edge('executor', 'broker', label='I/O Coordination', style='dashed')
dot.edge('broker', 'node', label='Node Management')
dot.edge('engine', 'shmem', label='Metadata Access', style='dotted')
dot.edge('engine', 'simple', label='Metadata Access', style='dotted')
dot.edge('engine', 'fdb', label='Metadata Access', style='dotted')
dot.edge('dagger', 'rundag', label='Plugin Hook', dir='both')
dot.edge('remotemonitor', 'engine', label='Monitoring', dir='both', style='dashed')
dot.edge('foundationdb', 'fdb', label='Persistent Storage', dir='both')

# Fault tolerance and performance annotations
dot.node('ft', 'Fault Tolerance\n(Failure Detection & Recovery)', shape='note', color='lightcoral')
dot.node('perf', 'Performance\n(Data Locality, Async Execution)', shape='note', color='lightgreen')
dot.edge('ft', 'engine', style='invis')
dot.edge('perf', 'scheduler', style='invis')

dot.render('dagscheduler_architecture', format='png', cleanup=True)
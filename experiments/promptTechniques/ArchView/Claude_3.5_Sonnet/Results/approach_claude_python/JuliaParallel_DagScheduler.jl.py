import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='DagScheduler Architecture View')
dot.attr(rankdir='TB')

# Add nodes with different shapes/styles
dot.attr('node', shape='box', style='rounded')
dot.node('DagScheduler', 'DagScheduler.jl\nMain Module')

# Core Components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components')
    core.node('RunEnv', 'RunEnv\nExecution Environment')
    core.node('Scheduler', 'Scheduler\nTask Scheduling')
    core.node('Engine', 'Execution Engine')

# Metadata Stores
with dot.subgraph(name='cluster_meta') as meta:
    meta.attr(label='Metadata Stores')
    meta.node('ShmemMeta', 'ShmemMetaStore\nShared Memory')
    meta.node('SimpleMeta', 'SimpleMetaStore\nCluster-wide')
    meta.node('FDBMeta', 'FDBMetaStore\nPersistent Storage')

# Execution Components
with dot.subgraph(name='cluster_exec') as exec:
    exec.attr(label='Execution Layer')
    exec.node('Node', 'Node\nPhysical Machine')
    exec.node('Broker', 'Broker\nNode Coordinator')
    exec.node('Executor', 'Executor\nTask Execution')

# Add edges
dot.edge('DagScheduler', 'RunEnv')
dot.edge('RunEnv', 'Scheduler')
dot.edge('Scheduler', 'Engine')
dot.edge('Engine', 'ShmemMeta')
dot.edge('Engine', 'SimpleMeta')
dot.edge('Engine', 'FDBMeta')
dot.edge('Engine', 'Node')
dot.edge('Node', 'Broker')
dot.edge('Broker', 'Executor')

# Set graph attributes
dot.attr(size='8,8')
dot.attr(dpi='300')

if __name__ == "__main__":
    dot.render('dagscheduler_architecture', format='png', cleanup=True)
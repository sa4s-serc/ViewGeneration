from graphviz import Digraph

# Initialize the diagram
dot = Digraph(comment='DagScheduler.jl Architecture')

# Define node styles
node_styles = {
    'nodes': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightblue'},
    'brokers': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgrey'},
    'executors': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgreen'},
    'metadata': {'shape': 'cylinder', 'style': 'filled', 'fillcolor': 'lightyellow'},
    'plugins': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightpink'},
    'files': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightcoral'},
}

# Add nodes for the main components
dot.node('Nodes', 'Nodes', **node_styles['nodes'])
dot.node('Brokers', 'Brokers', **node_styles['brokers'])
dot.node('Executors', 'Executors', **node_styles['executors'])
dot.node('MetaStore', 'MetaStore', **node_styles['metadata'])
dot.node('Plugins', 'Dagger.jl Plugin', **node_styles['plugins'])

# Add nodes for important files
dot.node('DagScheduler', 'DagScheduler.jl', **node_styles['files'])
dot.node('Common', 'common.jl', **node_styles['files'])
dot.node('Scheduler', 'scheduler.jl', **node_styles['files'])
dot.node('Engine', 'engine.jl', **node_styles['files'])
dot.node('Queue', 'queue.jl', **node_styles['files'])
dot.node('MetaStores', 'meta_stores/*', **node_styles['files'])
dot.node('PluginFile', 'plugin.jl', **node_styles['files'])

# Define edges between the components
dot.edge('Nodes', 'Brokers', label='coordinates tasks', dir='both')
dot.edge('Brokers', 'Executors', label='executes tasks', dir='both')
dot.edge('Executors', 'MetaStore', label='updates metadata', dir='both')
dot.edge('MetaStore', 'Brokers', label='notifies changes', dir='both')
dot.edge('DagScheduler', 'Common', label='defines structures', style='dashed')
dot.edge('DagScheduler', 'Scheduler', label='scheduling logic', style='dashed')
dot.edge('DagScheduler', 'Engine', label='execution engine', style='dashed')
dot.edge('DagScheduler', 'Queue', label='task assignment', style='dashed')
dot.edge('DagScheduler', 'MetaStores', label='metadata implementations', style='dashed')
dot.edge('DagScheduler', 'PluginFile', label='plugin integration', style='dashed')
dot.edge('Plugins', 'DagScheduler', label='uses as plugin', dir='both')

# Render the diagram
dot.render('dagscheduler_architecture', format='png', cleanup=True)
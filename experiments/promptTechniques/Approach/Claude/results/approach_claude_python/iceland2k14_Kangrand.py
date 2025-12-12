import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Software Architecture View')
dot.attr(rankdir='TB')

# Add nodes with different shapes and colors
dot.node('kangaroo', 'Kangaroo Class\n(Core Algorithm)', shape='box', style='filled', fillcolor='lightblue')
dot.node('secp256k1', 'SECP256K1 Class\n(Curve Operations)', shape='box', style='filled', fillcolor='lightgreen')
dot.node('gpu_engine', 'GPU Engine\n(CUDA)', shape='box', style='filled', fillcolor='lightpink')
dot.node('hash_table', 'Hash Table\n(DP Storage)', shape='box', style='filled', fillcolor='lightyellow')
dot.node('network', 'Network Component\n(Client/Server)', shape='box', style='filled', fillcolor='lightgrey')
dot.node('backup', 'Backup Component', shape='box', style='filled', fillcolor='lightcyan')
dot.node('thread', 'Thread Management', shape='box', style='filled', fillcolor='peachpuff')
dot.node('timer', 'Timer', shape='box', style='filled', fillcolor='lightgoldenrod')
dot.node('int_arith', 'Integer Arithmetic', shape='box', style='filled', fillcolor='palegreen')

# Add edges with labels
dot.edge('kangaroo', 'secp256k1', 'uses')
dot.edge('kangaroo', 'gpu_engine', 'manages')
dot.edge('kangaroo', 'hash_table', 'stores/retrieves')
dot.edge('kangaroo', 'network', 'communicates')
dot.edge('kangaroo', 'backup', 'saves/loads')
dot.edge('kangaroo', 'thread', 'controls')
dot.edge('secp256k1', 'int_arith', 'uses')
dot.edge('gpu_engine', 'thread', 'uses')
dot.edge('hash_table', 'backup', 'persistence')
dot.edge('timer', 'kangaroo', 'measures')

# Add subgraph for computational components
with dot.subgraph(name='cluster_compute') as c:
    c.attr(label='Computational Core')
    c.attr(style='rounded')
    c.node('secp256k1')
    c.node('gpu_engine')
    c.node('int_arith')

# Set graph attributes
dot.attr(label='Pollard\'s Kangaroo ECDLP Solver Architecture')
dot.attr(fontsize='16')

# Save the graph
dot.render('architecture_view', format='png', cleanup=True)
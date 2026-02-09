import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Software Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('text_proc', 'Text Processing\n(golang.org/x/text)')
dot.node('sys_int', 'System Interaction\n(golang.org/x/sys)')
dot.node('cli', 'CLI Tools\n(github.com/spf13/cobra)')

# Add subcomponents for text processing
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Text Processing Components')
    c.node('unicode_norm', 'Unicode\nNormalization')
    c.node('collation', 'Collation')
    c.node('bidi', 'BiDi Text\nHandling')
    c.node('idna', 'IDNA')
    c.node('encoding', 'Character\nEncoding')
    c.node('gotext', 'gotext Tool')

# Add subcomponents for system interaction
with dot.subgraph(name='cluster_1') as c:
    c.attr(label='System Interaction Components')
    c.node('os_abs', 'OS Abstraction')
    c.node('sys_calls', 'System Calls')
    c.node('win_api', 'Windows API\nBinding')

# Add subcomponents for CLI
with dot.subgraph(name='cluster_2') as c:
    c.attr(label='CLI Components')
    c.node('hier_cmd', 'Hierarchical\nCommands')
    c.node('args_flags', 'Arguments &\nFlags')
    c.node('cmd_gen', 'Command-Line\nGenerator')

# Add relationships
dot.edge('text_proc', 'unicode_norm')
dot.edge('text_proc', 'collation')
dot.edge('text_proc', 'bidi')
dot.edge('text_proc', 'idna')
dot.edge('text_proc', 'encoding')
dot.edge('text_proc', 'gotext')

dot.edge('sys_int', 'os_abs')
dot.edge('sys_int', 'sys_calls')
dot.edge('sys_int', 'win_api')

dot.edge('cli', 'hier_cmd')
dot.edge('cli', 'args_flags')
dot.edge('cli', 'cmd_gen')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr('graph', splines='ortho')

# Save the diagram
dot.render('architecture_view', format='png', cleanup=True)
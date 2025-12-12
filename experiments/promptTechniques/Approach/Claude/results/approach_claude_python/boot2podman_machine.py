import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Podman Machine Architecture')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('cli', 'CLI Commands\n(create, start, stop, rm, env, ssh)', shape='rectangle')
dot.node('libmachine', 'Libmachine\n(Core Library)', shape='rectangle')
dot.node('drivers', 'Drivers\n(VirtualBox, QEMU, Generic)', shape='rectangle')
dot.node('provisioners', 'Provisioners\n(RedHat, Fedora, CentOS)', shape='rectangle')
dot.node('host', 'Host\n(VM Configuration)', shape='rectangle')
dot.node('config', 'Configuration Files\n(TLS Certificates)', shape='rectangle')
dot.node('network', 'Network Components\n(Netfilter, NFTables)', shape='rectangle')

# Add edges to show relationships
dot.edge('cli', 'libmachine', 'uses')
dot.edge('libmachine', 'drivers', 'manages')
dot.edge('libmachine', 'provisioners', 'uses')
dot.edge('libmachine', 'host', 'creates/manages')
dot.edge('host', 'config', 'stores')
dot.edge('host', 'network', 'configures')
dot.edge('drivers', 'host', 'controls')
dot.edge('provisioners', 'host', 'configures')

# Add subgraph for driver plugins
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Driver Plugins')
    c.node('vbox', 'VirtualBox')
    c.node('qemu', 'QEMU')
    c.node('generic', 'Generic')
    c.attr('node', shape='box')
    dot.edge('drivers', 'vbox')
    dot.edge('drivers', 'qemu')
    dot.edge('drivers', 'generic')

# Generate the diagram
dot.render('podman_machine_architecture', format='png', cleanup=True)
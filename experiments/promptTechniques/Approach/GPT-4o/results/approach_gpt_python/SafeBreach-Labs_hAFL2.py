from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='hAFL2 Architectural View', format='png')

# Define node styles
node_attrs = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightgrey'}
vm_attrs = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightblue'}
driver_attrs = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightgreen'}
component_attrs = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightyellow'}

# Add nodes for VMs
dot.node('VM1', 'Linux Host (QEMU)', **vm_attrs)
dot.node('VM2', 'Root Partition (Windows VM)', **vm_attrs)
dot.node('VM3', 'Child Partition (Windows VM)', **vm_attrs)

# Add nodes for core components
dot.node('kAFL', 'kAFL Fuzzer', **component_attrs)
dot.node('KVM', 'Modified KVM', **component_attrs)
dot.node('IntelPT', 'Intel PT', **component_attrs)
dot.node('Redqueen', 'Redqueen Instrumentation', **component_attrs)

# Add nodes for drivers
dot.node('CPHarness', 'CPHarness.sys', **driver_attrs)
dot.node('CrashMonitoring', 'CrashMonitoringDriver.sys', **driver_attrs)

# Add edges for communication
dot.edge('VM1', 'VM2', label='Hosts', style='dashed')
dot.edge('VM2', 'VM3', label='Hosts', style='dashed')
dot.edge('VM3', 'CPHarness', label='Sends RNDIS packets')
dot.edge('CPHarness', 'VM2', label='To VMSwitch')
dot.edge('CrashMonitoring', 'kAFL', label='Reports crash info', dir='both')
dot.edge('kAFL', 'KVM', label='Controls via hypercalls')
dot.edge('KVM', 'IntelPT', label='Enables PT')
dot.edge('kAFL', 'Redqueen', label='Integrates', dir='both')

# Add subgraph for kAFL components
with dot.subgraph(name='cluster_kAFL') as c:
    c.attr(label='kAFL Components')
    c.node('kafl_fuzz', 'kafl_fuzz.py')
    c.node('kafl_gui', 'kafl_gui.py')
    c.node('kafl_master', 'master.py')
    c.node('kafl_slave', 'slave.py')
    c.node('kafl_tools', 'kafl_cov.py, kafl_debug.py, kafl_plot.py')
    c.edge('kafl_fuzz', 'kafl_master', label='Launches')
    c.edge('kafl_master', 'kafl_slave', label='Manages & Distributes')
    c.edge('kafl_slave', 'kafl_tools', label='Uses')

# Render the graph to a file
dot.render('hAFL2_architecture')
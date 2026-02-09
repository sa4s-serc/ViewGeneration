import graphviz

# Create a new directed graph
dot = graphviz.Digraph('hAFL2_Architecture', 
                       comment='hAFL2 Hypervisor Fuzzing Architecture',
                       format='png')

# Set global graph attributes
dot.attr(rankdir='TB', splines='ortho')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightgray')

# Create clusters/subgraphs
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Fuzzing Infrastructure', style='rounded', color='blue')
    c.node('fuzzer_master', 'Master\nProcess\n(kafl_fuzz.py)')
    c.node('fuzzer_slave', 'Slave\nProcesses\n(slave.py)')
    c.node('fuzzer_gui', 'GUI Monitor\n(kafl_gui.py)')
    c.edge('fuzzer_master', 'fuzzer_slave', 'Distributes\ntasks')
    c.edge('fuzzer_master', 'fuzzer_gui', 'Reports\nstatus')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Virtualization Layer', style='rounded', color='red')
    c.node('qemu_kvm', 'QEMU/KVM\nHost')
    c.node('root_vm', 'Root Partition\n(Windows VM)')
    c.node('child_vm', 'Child Partition\n(Windows VM)')
    c.edge('qemu_kvm', 'root_vm', 'Hosts')
    c.edge('root_vm', 'child_vm', 'Hosts')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Instrumentation & Monitoring', style='rounded', color='green')
    c.node('intel_pt', 'Intel PT\nCoverage')
    c.node('redqueen', 'Redqueen\nInstrumentation')
    c.node('crash_mon', 'CrashMonitoringDriver.sys')
    c.node('harness', 'CPHarness.sys')

# Add inter-cluster edges
dot.edge('fuzzer_slave', 'qemu_kvm', 'Controls')
dot.edge('intel_pt', 'root_vm', 'Traces\nexecution')
dot.edge('redqueen', 'root_vm', 'Instruments')
dot.edge('crash_mon', 'root_vm', 'Monitors\ncrashes')
dot.edge('harness', 'child_vm', 'Sends\ninputs')
dot.edge('harness', 'root_vm', 'Tests VSPs')
dot.edge('intel_pt', 'fuzzer_slave', 'Coverage\nfeedback')
dot.edge('redqueen', 'fuzzer_slave', 'Input\nfeedback')

# Save the diagram
dot.render('hafl2_architecture', view=True, cleanup=True)
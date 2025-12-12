import graphviz

# Create a new directed graph
dot = graphviz.Digraph('NASA cFS Architecture', comment='NASA cFS Architectural View')
dot.attr(rankdir='TB', splines='ortho')

# Define node styles
dot.attr('node', shape='box', style='filled,rounded', fillcolor='lightblue', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Create clusters/subgraphs
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core System Components', style='rounded', color='gray')
    core.node('cfe', 'Core Flight Executive (cFE)\nMicrokernel Architecture')
    core.node('osal', 'OS Abstraction Layer\n(OSAL)')
    core.node('psp', 'Platform Support Package\n(PSP)')

with dot.subgraph(name='cluster_apps') as apps:
    apps.attr(label='Lab Applications', style='rounded', color='gray')
    apps.node('es', 'Event Services')
    apps.node('cs', 'Command Services')
    apps.node('ts', 'Telemetry Services')
    apps.node('time', 'Time Services')

with dot.subgraph(name='cluster_cicd') as cicd:
    cicd.attr(label='CI/CD & Quality', style='rounded', color='gray')
    cicd.node('static', 'Static Analysis\nCodeQL/MISRA')
    cicd.node('test', 'Testing\nUnit/Functional')
    cicd.node('build', 'Build System\nCMake')

# Add relationships
# Core relationships
dot.edge('cfe', 'osal', 'uses')
dot.edge('osal', 'psp', 'abstracts')

# App relationships
dot.edge('es', 'cfe', 'depends on')
dot.edge('cs', 'cfe', 'depends on')
dot.edge('ts', 'cfe', 'depends on')
dot.edge('time', 'cfe', 'depends on')

# CI/CD relationships
dot.edge('static', 'test', 'precedes')
dot.edge('test', 'build', 'precedes')

# Set graph attributes
dot.attr(label='NASA Core Flight System (cFS)\nArchitectural View\nMicrokernel & Event-Driven Architecture')
dot.attr(fontname='Arial', fontsize='16')
dot.attr(labelloc='t')

# Save the diagram
dot.render('nasa_cfs_architecture', format='png', cleanup=True)
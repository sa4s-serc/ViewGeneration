import graphviz

# Create a new directed graph
dot = graphviz.Digraph('ClearML Agent Architecture')
dot.attr(rankdir='TB')
dot.attr('node', shape='box', style='rounded')

# Define node clusters
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Core Components')
    c.attr('node', color='#2B7CE9', style='filled,rounded', fontcolor='white')
    c.node('agent', 'ClearML Agent\nCore Execution')
    c.node('resource', 'Resource Monitor\nCPU/GPU/Memory')
    c.node('req', 'Requirements Manager\nPip/Conda/Poetry')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Integration Layer')
    c.attr('node', color='#E6550D', style='filled,rounded', fontcolor='white')
    c.node('docker', 'Docker Integration')
    c.node('k8s', 'K8s/SLURM\nIntegration')
    c.node('config', 'Configuration\nSystem (HOCON)')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='External Systems')
    c.attr('node', color='#31A354', style='filled,rounded', fontcolor='white')
    c.node('server', 'ClearML Server\nExperiment Management')
    c.node('registry', 'Container Registry')

# Define edges
dot.edge('server', 'agent', 'Pull Tasks')
dot.edge('agent', 'req', 'Setup Environment')
dot.edge('req', 'docker', 'Build Environment')
dot.edge('docker', 'registry', 'Pull Images')
dot.edge('agent', 'docker', 'Execute Tasks')
dot.edge('agent', 'k8s', 'Submit Jobs')
dot.edge('resource', 'agent', 'Report Metrics')
dot.edge('agent', 'server', 'Report Status')
dot.edge('config', 'agent', 'Configure')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr(rankdir='TB')
dot.attr(splines='ortho')

# Save the diagram
dot.render('clearml_architecture', format='png', cleanup=True)
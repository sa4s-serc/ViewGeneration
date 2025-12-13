from graphviz import Digraph

dot = Digraph('Software_Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('cli', 'CLI Interface\n(cmd/sneaker/main.go)')
dot.node('manager', 'Manager\n(sneaker.go)')
dot.node('envelope', 'Envelope\n(envelope.go)')
dot.node('s3', 'S3 Interface\n(ObjectStorage)')
dot.node('kms', 'KMS Interface\n(KeyManagement)')

# Core operations nodes
dot.node('upload', 'Upload\n(upload.go)')
dot.node('download', 'Download\n(download.go)')
dot.node('list', 'List\n(list.go)')
dot.node('rm', 'Remove\n(rm.go)')
dot.node('pack', 'Pack\n(pack.go)')
dot.node('unpack', 'Unpack\n(unpack.go)')
dot.node('rotate', 'Rotate\n(rotate.go)')

# Add edges
dot.edge('cli', 'manager', 'commands')
dot.edge('manager', 'envelope', 'uses')
dot.edge('manager', 's3', 'implements')
dot.edge('manager', 'kms', 'implements')
dot.edge('envelope', 'kms', 'encryption')

# Connect operations to manager
dot.edge('manager', 'upload', 'manages')
dot.edge('manager', 'download', 'manages')
dot.edge('manager', 'list', 'manages')
dot.edge('manager', 'rm', 'manages')
dot.edge('manager', 'pack', 'manages')
dot.edge('manager', 'unpack', 'manages')
dot.edge('manager', 'rotate', 'manages')

# Define subgraphs for visual grouping
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components')
    core.node('manager')
    core.node('envelope')

with dot.subgraph(name='cluster_interfaces') as interfaces:
    interfaces.attr(label='External Interfaces')
    interfaces.node('s3')
    interfaces.node('kms')

with dot.subgraph(name='cluster_operations') as operations:
    operations.attr(label='Operations')
    operations.node('upload')
    operations.node('download')
    operations.node('list')
    operations.node('rm')
    operations.node('pack')
    operations.node('unpack')
    operations.node('rotate')

dot.render('architecture_diagram', view=True, format='png')
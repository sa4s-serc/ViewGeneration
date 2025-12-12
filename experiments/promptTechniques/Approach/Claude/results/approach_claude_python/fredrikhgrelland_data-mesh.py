from graphviz import Digraph

dot = Digraph(comment='Data Mesh Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('minio', 'MinIO\nObject Storage')
dot.node('hive', 'Hive Metastore\nSchema Management')
dot.node('presto', 'Presto\nQuery Engine')
dot.node('sqlpad', 'SQLPad\nSQL IDE')
dot.node('nomad', 'Nomad\nOrchestration')
dot.node('consul', 'Consul\nService Discovery')
dot.node('terraform', 'Terraform\nInfrastructure as Code')
dot.node('ansible', 'Ansible\nConfiguration Management')
dot.node('vagrant', 'Vagrant\nDevelopment Environment')
dot.node('github', 'GitHub Actions\nCI/CD')

# Add relationships
dot.edge('minio', 'hive', 'Metadata')
dot.edge('hive', 'presto', 'Schema')
dot.edge('presto', 'sqlpad', 'Query Results')
dot.edge('nomad', 'minio', 'Manages')
dot.edge('nomad', 'hive', 'Manages')
dot.edge('nomad', 'presto', 'Manages')
dot.edge('nomad', 'sqlpad', 'Manages')
dot.edge('consul', 'nomad', 'Service Discovery')
dot.edge('terraform', 'nomad', 'Provisions')
dot.edge('ansible', 'terraform', 'Orchestrates')
dot.edge('vagrant', 'ansible', 'Provisions')
dot.edge('github', 'ansible', 'Triggers')

# Generate diagram
dot.render('data_mesh_architecture', view=True, format='png')
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Data Mesh Architecture')

# Add nodes for each core component
dot.node('MinIO', 'MinIO\nData Storage')
dot.node('Hive', 'Hive Metastore\nMetadata Management')
dot.node('Presto', 'Presto\nQuery Engine')
dot.node('SQLPad', 'SQLPad\nSQL IDE')
dot.node('Nomad', 'Nomad\nOrchestration')
dot.node('Consul', 'Consul\nService Discovery\nSecure Communication')
dot.node('Terraform', 'Terraform\nInfrastructure as Code')
dot.node('Vagrant', 'Vagrant\nDevelopment Environment')
dot.node('GitHub', 'GitHub Actions\nAutomated Testing')

# Add edges to represent connections and interactions
dot.edge('MinIO', 'Hive', 'Stores Metadata')
dot.edge('Hive', 'Presto', 'Schema Discovery')
dot.edge('Presto', 'SQLPad', 'SQL Queries')
dot.edge('Nomad', 'MinIO', 'Manage Deployment')
dot.edge('Nomad', 'Hive', 'Manage Deployment')
dot.edge('Nomad', 'Presto', 'Manage Deployment')
dot.edge('Nomad', 'SQLPad', 'Manage Deployment')
dot.edge('Nomad', 'Consul', 'Service Communication')
dot.edge('Terraform', 'Nomad', 'Provision Jobs')
dot.edge('Vagrant', 'Nomad', 'Environment Setup')
dot.edge('GitHub', 'Vagrant', 'Test & Lint Code')

# Render the graph to a file
dot.render('data_mesh_architecture', format='png', cleanup=True)
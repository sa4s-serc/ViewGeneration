from graphviz import Digraph

dot = Digraph(comment='Ethereum Node Deployment Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('geth', 'Geth\n(Execution Layer)')
dot.node('lighthouse', 'Lighthouse\n(Consensus Layer)')
dot.node('influxdb', 'InfluxDB\n(Metrics Storage)')
dot.node('nginx', 'Nginx\n(Reverse Proxy)')
dot.node('cloudbuild', 'Google Cloud Build\n(CI/CD)')
dot.node('k8s', 'Kubernetes\n(Container Orchestration)')
dot.node('secrets', 'Secret Manager\n(Credentials)')

# Add storage nodes
dot.node('geth_storage', 'Geth Storage\n(2000Gi)')
dot.node('lighthouse_storage', 'Lighthouse Storage\n(500Gi)')
dot.node('influxdb_storage', 'InfluxDB Storage')

# Define edges
dot.edge('geth', 'lighthouse', 'JWT Auth')
dot.edge('geth', 'influxdb', 'Metrics')
dot.edge('nginx', 'geth', 'RPC/WS')
dot.edge('nginx', 'influxdb', 'Metrics API')
dot.edge('cloudbuild', 'k8s', 'Deploy')
dot.edge('k8s', 'geth')
dot.edge('k8s', 'lighthouse')
dot.edge('k8s', 'influxdb')
dot.edge('k8s', 'nginx')
dot.edge('secrets', 'k8s', 'Inject Secrets')
dot.edge('geth', 'geth_storage')
dot.edge('lighthouse', 'lighthouse_storage')
dot.edge('influxdb', 'influxdb_storage')

# Render the graph
dot.render('ethereum_node_architecture', format='png', cleanup=True)
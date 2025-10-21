from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Turing Platform Architecture')

# Define nodes for services, sub-systems, and components
dot.node('A', 'API Server')
dot.node('B', 'Router Engine')
dot.node('C', 'Experiment Engine\n(Standard, Custom, Nop, Planout, Optimizely)')
dot.node('D', 'Batch Ensembler Engine')
dot.node('E', 'Prometheus & Alerting')
dot.node('F', 'Logging & Monitoring\n(BigQuery, Kafka, Fluentd, Jaeger)')
dot.node('G', 'Kubernetes Cluster')
dot.node('H', 'Helm Charts & Docker Compose')
dot.node('I', 'Python SDK')
dot.node('J', 'CI/CD Pipeline')
dot.node('K', 'Webhooks')
dot.node('L', 'ML Experimentation Platform\n(HTTP/JSON, UPI/gRPC)')

# Define edges for communication and control flow
dot.edge('A', 'B', label='REST API')
dot.edge('A', 'C', label='API Calls')
dot.edge('A', 'D', label='API Calls')
dot.edge('A', 'E', label='Alert Rules')
dot.edge('A', 'F', label='Log Data')
dot.edge('A', 'K', label='Trigger Webhooks')
dot.edge('B', 'L', label='Route Traffic')
dot.edge('C', 'L', label='Manage Experiments')
dot.edge('D', 'L', label='Batch Ensembling')
dot.edge('G', 'A', label='Deploy')
dot.edge('G', 'B', label='Deploy')
dot.edge('G', 'C', label='Deploy')
dot.edge('G', 'D', label='Deploy')
dot.edge('H', 'G', label='Deploy Infrastructure')
dot.edge('I', 'A', label='Interact with API')
dot.edge('J', 'A', label='Deploy Code')
dot.edge('J', 'B', label='Deploy Code')
dot.edge('J', 'C', label='Deploy Code')
dot.edge('J', 'D', label='Deploy Code')

# Render the diagram to a file
dot.render('turing_platform_architecture', format='png', cleanup=True)
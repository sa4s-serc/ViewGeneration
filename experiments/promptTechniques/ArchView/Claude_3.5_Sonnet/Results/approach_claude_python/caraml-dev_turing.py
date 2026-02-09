from graphviz import Digraph

dot = Digraph(comment='Turing Platform Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('api', 'API Server\n(REST/gRPC)')
dot.node('router', 'Router Engine\n(Traffic Management)')
dot.node('exp', 'Experiment Engine\n(A/B Testing)')
dot.node('batch', 'Batch Ensembler\n(Spark on K8s)')
dot.node('alert', 'Alerting System\n(Prometheus)')
dot.node('log', 'Logging System\n(BigQuery/Kafka)')
dot.node('trace', 'Tracing\n(Jaeger)')
dot.node('mlp', 'MLP Integration')
dot.node('k8s', 'Kubernetes\nInfrastructure')

# Add connections
dot.edge('api', 'router', 'HTTP/gRPC')
dot.edge('router', 'exp', 'Experiment Config')
dot.edge('router', 'batch', 'Model Ensemble')
dot.edge('api', 'alert', 'Monitoring')
dot.edge('api', 'log', 'Events')
dot.edge('api', 'trace', 'Traces')
dot.edge('router', 'mlp', 'Model Info')
dot.edge('batch', 'k8s', 'Spark Jobs')
dot.edge('router', 'k8s', 'Deployments')

# Add subgraph for data stores
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Storage')
    c.node('config', 'Config Store')
    c.node('results', 'Results Store')
    
dot.edge('router', 'config', 'Read')
dot.edge('batch', 'results', 'Write')
dot.edge('router', 'results', 'Read/Write')

dot.render('turing_architecture', view=True, format='png')
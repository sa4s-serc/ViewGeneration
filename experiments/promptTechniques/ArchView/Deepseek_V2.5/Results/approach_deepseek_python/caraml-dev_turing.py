import graphviz

dot = graphviz.Digraph(comment='Turing Platform Architecture')
dot.attr(rankdir='TB', size='8,8')

with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Turing Platform', style='filled', color='lightgrey')
    c.node('API', 'API Server', shape='ellipse')
    c.node('Router', 'Router Engine', shape='box')
    c.node('Experiment', 'Experiment Engine', shape='box')
    c.node('Batch', 'Batch Ensembler Engine', shape='box')
    c.node('SDK', 'Python SDK', shape='ellipse')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='External Services', style='filled', color='lightblue')
    c.node('Merlin', 'Merlin', shape='box')
    c.node('MLP', 'MLP', shape='box')
    c.node('Prometheus', 'Prometheus', shape='box')
    c.node('Jaeger', 'Jaeger', shape='box')
    c.node('BigQuery', 'BigQuery', shape='box')
    c.node('Kafka', 'Kafka', shape='box')
    c.node('Spark', 'Spark on K8s', shape='box')

dot.edge('SDK', 'API', label='REST API')
dot.edge('API', 'Router', label='deploy')
dot.edge('API', 'Experiment', label='configure')
dot.edge('API', 'Batch', label='submit')
dot.edge('Router', 'Experiment', label='integrate')
dot.edge('Router', 'Merlin', label='call')
dot.edge('Router', 'MLP', label='call')
dot.edge('Router', 'Prometheus', label='metrics')
dot.edge('Router', 'Jaeger', label='tracing')
dot.edge('Router', 'BigQuery', label='logs')
dot.edge('Router', 'Kafka', label='logs')
dot.edge('Batch', 'Spark', label='run job')

dot.render('turing_architecture', format='png', cleanup=True)
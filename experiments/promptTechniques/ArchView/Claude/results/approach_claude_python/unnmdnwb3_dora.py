from graphviz import Digraph

dot = Digraph(comment='DORA Metrics Automation Tool Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('api', 'Backend API\n(Gin-Gonic)')
dot.node('db', 'MongoDB')
dot.node('gitlab', 'GitLab\nConnector')
dot.node('prom', 'Prometheus\nConnector')
dot.node('calc', 'Metrics\nCalculation\nService')

# Add subcomponents for metrics
with dot.subgraph(name='cluster_metrics') as c:
    c.attr(label='DORA Metrics')
    c.node('df', 'Deployment\nFrequency')
    c.node('lt', 'Lead Time\nfor Changes')
    c.node('cfr', 'Change\nFailure Rate')
    c.node('mttr', 'Mean Time\nto Restore')

# Define relationships
dot.edge('gitlab', 'api', 'Fetch Git Data')
dot.edge('prom', 'api', 'Alert Data')
dot.edge('api', 'db', 'Store Data')
dot.edge('db', 'calc', 'Retrieve Data')
dot.edge('calc', 'df')
dot.edge('calc', 'lt')
dot.edge('calc', 'cfr')
dot.edge('calc', 'mttr')

# External connections
dot.node('ext_gitlab', 'GitLab', shape='cloud')
dot.node('ext_prom', 'Prometheus', shape='cloud')
dot.edge('ext_gitlab', 'gitlab', 'API Calls')
dot.edge('ext_prom', 'prom', 'Query Metrics')

# Set graph attributes
dot.attr(fontsize='12')
dot.attr(size='8,8')

# Generate the diagram
dot.render('dora_architecture', format='png', cleanup=True)
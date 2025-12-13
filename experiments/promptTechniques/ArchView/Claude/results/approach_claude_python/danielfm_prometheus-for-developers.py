import graphviz

# Create a new directed graph
g = graphviz.Digraph('Prometheus_Architecture')
g.attr(rankdir='TB')

# Define node styles
g.attr('node', shape='box', style='rounded', fontname='Arial', fontsize='10')
g.attr('edge', fontname='Arial', fontsize='9')

# Add nodes
g.node('app', 'Sample Node.js App\n(/metrics endpoint)', color='lightblue', style='filled')
g.node('prometheus', 'Prometheus Server\n(Time Series DB)', color='orange', style='filled')
g.node('alertmanager', 'Alertmanager\n(Alert Handling)', color='red', style='filled')
g.node('grafana', 'Grafana\n(Visualization)', color='green', style='filled')

# Add edges with descriptions
g.edge('prometheus', 'app', 'scrapes metrics\nevery 15s')
g.edge('prometheus', 'alertmanager', 'sends\nalerts')
g.edge('prometheus', 'grafana', 'provides\nmetrics data')

# Create container for monitoring components
with g.subgraph(name='cluster_monitoring') as c:
    c.attr(label='Monitoring Stack', style='dashed', color='gray')
    c.node('prometheus')
    c.node('alertmanager')
    c.node('grafana')

# Add configuration nodes
g.node('prom_config', 'prometheus.yml\n(Configuration)', shape='note', color='lightgray', style='filled')
g.node('alert_rules', 'prometheus.rules.yml\n(Alert Rules)', shape='note', color='lightgray', style='filled')
g.node('grafana_ds', 'datasource.yml\n(Grafana Config)', shape='note', color='lightgray', style='filled')

# Connect configurations
g.edge('prom_config', 'prometheus', 'configures')
g.edge('alert_rules', 'prometheus', 'defines\nalerts')
g.edge('grafana_ds', 'grafana', 'configures')

# Save the diagram
g.render('prometheus_architecture', format='png', cleanup=True)
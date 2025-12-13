import graphviz as gv

dot = gv.Digraph('Wonko Architecture', 
                 comment='Wonko Monitoring Service Architecture',
                 format='png')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add service components
dot.node('wonko_core', 'Wonko Core\nService')
dot.node('kafka', 'Kafka\nMessage Bus')
dot.node('prometheus', 'Prometheus\nMetrics')
dot.node('pagerduty', 'PagerDuty\nAlerts')

# Add client services
dot.node('krikkit', 'Krikkit\nService')
dot.node('eccentrica', 'Eccentrica\nService')

# Add key components
dot.node('web_server', 'Web Server\n(Ring/Compojure)')
dot.node('alert_processor', 'Alert\nProcessor')
dot.node('metrics_exporter', 'Metrics\nExporter')

# Define edges
dot.edge('krikkit', 'kafka', 'events')
dot.edge('eccentrica', 'kafka', 'events')
dot.edge('kafka', 'wonko_core', 'consume')
dot.edge('wonko_core', 'alert_processor', 'process')
dot.edge('alert_processor', 'pagerduty', 'notify')
dot.edge('wonko_core', 'metrics_exporter', 'export')
dot.edge('metrics_exporter', 'prometheus', 'expose')
dot.edge('web_server', 'prometheus', 'scrape endpoint')

# Add subgraph for monitoring components
with dot.subgraph(name='cluster_monitoring') as monitoring:
    monitoring.attr(label='Monitoring Components')
    monitoring.node('metrics_store', 'Metrics\nStorage')
    monitoring.node('alert_rules', 'Alert\nRules')
    dot.edge('metrics_exporter', 'metrics_store', 'store')
    dot.edge('alert_rules', 'alert_processor', 'evaluate')

dot.render('wonko_architecture', view=True)
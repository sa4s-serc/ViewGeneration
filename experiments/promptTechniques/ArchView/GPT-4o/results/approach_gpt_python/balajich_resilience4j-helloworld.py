from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Resilience4j-Helloworld Architecture')

# Define nodes for services
dot.node('A', 'Service A', shape='box')
dot.node('B', 'Service B', shape='box')

# Define nodes for resilience patterns
dot.node('CB', 'Circuit Breaker', shape='ellipse')
dot.node('RL', 'Rate Limiter', shape='ellipse')
dot.node('BH', 'Bulkhead', shape='ellipse')
dot.node('RT', 'Retry', shape='ellipse')
dot.node('TL', 'TimeLimiter', shape='ellipse')

# Define nodes for monitoring and configuration
dot.node('MON', 'Prometheus & Grafana', shape='box')
dot.node('CFG', 'Configurations (application.yml)', shape='box')

# Define edges for communication
dot.edge('A', 'B', label='REST API', style='dashed')
dot.edge('A', 'CB', label='@CircuitBreaker', style='dotted')
dot.edge('A', 'RL', label='@RateLimiter', style='dotted')
dot.edge('A', 'BH', label='@Bulkhead', style='dotted')
dot.edge('A', 'RT', label='@Retry', style='dotted')
dot.edge('A', 'TL', label='@TimeLimiter', style='dotted')
dot.edge('A', 'MON', label='Monitoring', style='dashed')
dot.edge('A', 'CFG', label='Configuration', style='dashed')

# Define edges for resilience pattern interactions
dot.edge('CB', 'RL', label='Combined', style='dotted')

# Render the graph
dot.render('resilience4j-helloworld-architecture', format='png', cleanup=True)
from graphviz import Digraph

dot = Digraph(comment='Resilience4j Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Create main components
dot.node('service_a', 'Service A\n(Spring Boot)')
dot.node('service_b', 'Service B\n(Spring Boot)')

# Create resilience pattern nodes
dot.node('circuit_breaker', 'Circuit Breaker\n@CircuitBreaker', color='blue')
dot.node('rate_limiter', 'Rate Limiter\n@RateLimiter', color='green')
dot.node('bulkhead', 'Bulkhead\n@Bulkhead', color='orange')
dot.node('retry', 'Retry\n@Retry', color='purple')
dot.node('time_limiter', 'Time Limiter\n@TimeLimiter', color='red')

# Create monitoring components
dot.node('prometheus', 'Prometheus\nMonitoring')
dot.node('grafana', 'Grafana\nDashboard')

# Add edges
dot.edge('service_a', 'circuit_breaker')
dot.edge('circuit_breaker', 'service_b')
dot.edge('service_a', 'rate_limiter')
dot.edge('rate_limiter', 'service_b')
dot.edge('service_a', 'bulkhead')
dot.edge('bulkhead', 'service_b')
dot.edge('service_a', 'retry')
dot.edge('retry', 'service_b')
dot.edge('service_a', 'time_limiter')
dot.edge('time_limiter', 'service_b')

# Monitoring edges
dot.edge('service_a', 'prometheus', style='dashed')
dot.edge('service_b', 'prometheus', style='dashed')
dot.edge('prometheus', 'grafana', style='dashed')

# Save the diagram
dot.render('resilience4j_architecture', format='png', cleanup=True)
import graphviz

dot = graphviz.Digraph(comment='Resilience4j-Helloworld Architecture')
dot.attr(rankdir='TB', size='8,8')

with dot.subgraph(name='cluster_service_a') as c:
    c.attr(label='Service A', style='rounded,filled', color='lightblue', fontsize='16')
    c.node('sa_circuitbreaker', 'Circuit Breaker', shape='ellipse', style='filled', color='lightcoral')
    c.node('sa_ratelimiter', 'Rate Limiter', shape='ellipse', style='filled', color='lightgreen')
    c.node('sa_bulkhead', 'Bulkhead', shape='ellipse', style='filled', color='lightyellow')
    c.node('sa_retry', 'Retry', shape='ellipse', style='filled', color='lightpink')
    c.node('sa_timelimiter', 'TimeLimiter', shape='ellipse', style='filled', color='lightcyan')
    c.node('sa_rest', 'REST API', shape='box', style='filled', color='white')

with dot.subgraph(name='cluster_service_b') as c:
    c.attr(label='Service B', style='rounded,filled', color='lightblue', fontsize='16')
    c.node('sb_rest', 'REST API', shape='box', style='filled', color='white')

dot.node('resilience4j', 'Resilience4j Library', shape='octagon', style='filled', color='orange')
dot.node('spring_boot', 'Spring Boot', shape='box', style='filled', color='purple', fontcolor='white')
dot.node('prometheus', 'Prometheus', shape='box', style='filled', color='red', fontcolor='white')
dot.node('grafana', 'Grafana', shape='box', style='filled', color='darkgreen', fontcolor='white')
dot.node('jmeter', 'JMeter', shape='box', style='filled', color='brown', fontcolor='white')
dot.node('docker', 'Docker', shape='box', style='filled', color='blue', fontcolor='white')
dot.node('vagrant', 'Vagrant', shape='box', style='filled', color='darkorange', fontcolor='white')

dot.edge('sa_rest', 'sb_rest', label='REST API Call', style='solid', color='black')
dot.edge('resilience4j', 'sa_circuitbreaker', style='dashed', color='gray')
dot.edge('resilience4j', 'sa_ratelimiter', style='dashed', color='gray')
dot.edge('resilience4j', 'sa_bulkhead', style='dashed', color='gray')
dot.edge('resilience4j', 'sa_retry', style='dashed', color='gray')
dot.edge('resilience4j', 'sa_timelimiter', style='dashed', color='gray')
dot.edge('spring_boot', 'sa_rest', style='dashed', color='gray')
dot.edge('spring_boot', 'sb_rest', style='dashed', color='gray')
dot.edge('sa_rest', 'prometheus', label='Metrics', style='dotted', color='red')
dot.edge('prometheus', 'grafana', label='Data', style='dotted', color='darkgreen')
dot.edge('jmeter', 'sa_rest', label='Load Testing', style='dashed', color='brown')
dot.edge('docker', 'sa_rest', style='dashed', color='blue')
dot.edge('docker', 'sb_rest', style='dashed', color='blue')
dot.edge('vagrant', 'docker', style='dashed', color='darkorange')

dot.render('resilience4j_architecture', format='png', cleanup=True)
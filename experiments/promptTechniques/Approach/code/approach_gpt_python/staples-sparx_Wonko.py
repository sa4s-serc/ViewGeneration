from graphviz import Digraph

dot = Digraph(comment='Wonko Monitoring and Alerting Service')

# Define nodes
dot.node('A', 'Wonko Monitoring Service', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('B', 'Kafka', shape='cylinder', style='filled', fillcolor='lightblue')
dot.node('C', 'Prometheus', shape='cylinder', style='filled', fillcolor='lightgreen')
dot.node('D', 'PagerDuty', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('E', 'Krikkit Service', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('F', 'Eccentrica Service', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('G', 'HTTP API', shape='rectangle', style='dashed')

# Define edges
dot.edge('E', 'B', label='Produce Events', dir='forward', style='dotted')
dot.edge('F', 'B', label='Produce Events', dir='forward', style='dotted')
dot.edge('B', 'A', label='Consume Events', dir='forward', style='dotted')
dot.edge('A', 'C', label='Expose Metrics', dir='forward', style='dotted')
dot.edge('A', 'D', label='Trigger Alerts', dir='forward', style='dotted')
dot.edge('A', 'G', label='Metrics Endpoint', dir='forward', style='dotted')

# Legend
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Legend', style='dotted')
    c.node('X', 'Microservice', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('Y', 'Queue/Stream', shape='cylinder', style='filled', fillcolor='lightblue')
    c.node('Z', 'External Service/API', shape='rectangle', style='filled', fillcolor='lightpink')
    c.node('W', 'Internal Service', shape='rectangle', style='filled', fillcolor='lightgrey')

dot.render('wonko_architecture', format='png', cleanup=True)
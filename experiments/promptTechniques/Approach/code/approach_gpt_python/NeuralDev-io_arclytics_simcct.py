from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Arclytics SimCCT Architecture')

# Define nodes for services, databases, and other components
dot.node('Client', 'React Client', shape='rect', style='filled', fillcolor='lightblue')
dot.node('SimCCT Service', 'Flask-based SimCCT Service', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('MongoDB', 'MongoDB', shape='cylinder', style='filled', fillcolor='lightyellow')
dot.node('Redis', 'Redis', shape='cylinder', style='filled', fillcolor='lightyellow')
dot.node('Celery', 'Celery Worker', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('Fluentd', 'Fluentd Logger', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('Elasticsearch', 'Elasticsearch', shape='cylinder', style='filled', fillcolor='lightyellow')
dot.node('Kibana', 'Kibana Dashboard', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('API Gateway', 'API Gateway', shape='rect', style='filled', fillcolor='lightgray')

# Define communication between components
dot.edge('Client', 'API Gateway', label='REST API', style='solid')
dot.edge('API Gateway', 'SimCCT Service', label='REST API', style='dashed')
dot.edge('SimCCT Service', 'MongoDB', label='Data Access', style='dotted')
dot.edge('SimCCT Service', 'Redis', label='Session/Caching', style='dotted')
dot.edge('SimCCT Service', 'Celery', label='Task Queue', style='dashed')
dot.edge('SimCCT Service', 'Fluentd', label='Logging', style='dotted')
dot.edge('Fluentd', 'Elasticsearch', label='Log Storage', style='dashed')
dot.edge('Elasticsearch', 'Kibana', label='Visualization', style='dotted')

# Render the diagram (this will create a file named 'Arclytics_SimCCT_Architecture.gv')
dot.render('Arclytics_SimCCT_Architecture', format='png', cleanup=True)
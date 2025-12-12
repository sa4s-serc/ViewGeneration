from graphviz import Digraph

dot = Digraph(comment='Streaming Service with Microservices Architecture')

# Adding nodes
dot.node('A', 'movies_streaming_converter (FFmpeg)', shape='rectangle', style='filled', color='lightblue')
dot.node('B', 'movies_streaming_etl (Apache Airflow)', shape='rectangle', style='filled', color='lightblue')
dot.node('C', 'movies_auth (JWT, Google OAuth)', shape='rectangle', style='filled', color='lightblue')
dot.node('D', 'movies_billing (Stripe)', shape='rectangle', style='filled', color='lightblue')
dot.node('E', 'movies_async_api (Elasticsearch, Redis)', shape='rectangle', style='filled', color='lightblue')
dot.node('F', 'movies_admin (Django)', shape='rectangle', style='filled', color='lightblue')
dot.node('G', 'movies_streaming_admin (Django)', shape='rectangle', style='filled', color='lightblue')
dot.node('H', 'movies_ugc (Kafka, ClickHouse)', shape='rectangle', style='filled', color='lightblue')

# Adding databases
dot.node('DB1', 'PostgreSQL', shape='cylinder', style='filled', color='lightgrey')
dot.node('DB2', 'Elasticsearch', shape='cylinder', style='filled', color='lightgrey')
dot.node('DB3', 'Redis', shape='cylinder', style='filled', color='lightgrey')
dot.node('DB4', 'ClickHouse', shape='cylinder', style='filled', color='lightgrey')
dot.node('O', 'MinIO', shape='rectangle', style='filled', color='lightgrey')

# Adding edges
dot.edge('A', 'B', label='Video Conversion', arrowhead='normal')
dot.edge('B', 'DB1', label='ETL Tasks', arrowhead='normal')
dot.edge('C', 'D', label='Auth & Billing', arrowhead='normal')
dot.edge('E', 'DB2', label='Search', arrowhead='normal')
dot.edge('E', 'DB3', label='Cache', arrowhead='normal')
dot.edge('H', 'DB4', label='UGC Events & Storage', arrowhead='normal')
dot.edge('H', 'O', label='Media Storage', arrowhead='normal')

# Adding styles to nodes for clarity
dot.attr('node', shape='rectangle', style='filled', color='lightblue')

# Visualizing the microservices architecture
dot.render('streaming_service_microservices_architecture', format='png', cleanup=True)
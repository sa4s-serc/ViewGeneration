import graphviz

dot = graphviz.Digraph(comment='Streaming Service Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('auth', 'Authentication Service\n(movies_auth)\nJWT, OAuth')
dot.node('billing', 'Billing Service\n(movies_billing)\nStripe Integration')
dot.node('async_api', 'Async API Service\n(movies_async_api)\nFastAPI')
dot.node('admin', 'Admin Service\n(movies_admin)\nDjango')
dot.node('etl', 'ETL Pipeline\n(movies_streaming_etl)\nAirflow')
dot.node('converter', 'Converter Service\n(movies_streaming_converter)\nFFmpeg')
dot.node('ugc', 'UGC Service\n(movies_ugc)\nUser Activity')

# Add databases
dot.attr('node', shape='cylinder')
dot.node('postgres', 'PostgreSQL')
dot.node('elastic', 'Elasticsearch')
dot.node('redis', 'Redis Cache')
dot.node('clickhouse', 'ClickHouse')
dot.node('minio', 'MinIO\nObject Storage')

# Add message brokers
dot.attr('node', shape='hexagon')
dot.node('kafka', 'Kafka')
dot.node('rabbitmq', 'RabbitMQ')

# Add connections
dot.edge('auth', 'postgres')
dot.edge('billing', 'postgres')
dot.edge('async_api', 'elastic')
dot.edge('async_api', 'redis')
dot.edge('admin', 'postgres')
dot.edge('etl', 'minio')
dot.edge('etl', 'rabbitmq')
dot.edge('converter', 'minio')
dot.edge('converter', 'rabbitmq')
dot.edge('ugc', 'kafka')
dot.edge('ugc', 'clickhouse')
dot.edge('async_api', 'kafka')

print(dot.source)
dot.render('streaming_service_architecture', view=True, format='png')
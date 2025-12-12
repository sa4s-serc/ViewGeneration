from graphviz import Digraph

dot = Digraph(comment='SWIR Sidecar Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Create main components
dot.node('app', 'Application\n(Business Logic)')
dot.node('http_handler', 'HTTP Handler')
dot.node('grpc_handler', 'gRPC Handler')
dot.node('si_handler', 'Service Invocation\nHandler')
dot.node('msg_handler', 'Messaging Handler')
dot.node('persist_handler', 'Persistence Handler')
dot.node('service_disc', 'Service Discovery\n(mDNS/DynamoDB)')

# Create external services
dot.attr('node', shape='rectangle', style='rounded,dashed')
dot.node('kafka', 'Kafka')
dot.node('nats', 'NATS')
dot.node('kinesis', 'AWS Kinesis')
dot.node('redis', 'Redis')
dot.node('dynamodb', 'DynamoDB')
dot.node('services', 'External Services')

# Create connections
dot.edge('app', 'http_handler')
dot.edge('app', 'grpc_handler')
dot.edge('http_handler', 'si_handler')
dot.edge('http_handler', 'msg_handler')
dot.edge('http_handler', 'persist_handler')
dot.edge('grpc_handler', 'si_handler')
dot.edge('grpc_handler', 'msg_handler')
dot.edge('grpc_handler', 'persist_handler')
dot.edge('si_handler', 'service_disc')
dot.edge('service_disc', 'services')
dot.edge('msg_handler', 'kafka')
dot.edge('msg_handler', 'nats')
dot.edge('msg_handler', 'kinesis')
dot.edge('persist_handler', 'redis')
dot.edge('persist_handler', 'dynamodb')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('swir_architecture', view=True, format='png')
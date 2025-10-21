from graphviz import Digraph

dot = Digraph(comment='Teamgram Server Architecture', format='png')

# Define nodes for services
dot.node('BFF', 'Backend for Frontend (BFF)', shape='rectangle')
dot.node('MSG', 'Message Service', shape='rectangle')
dot.node('CHAT', 'Chat Management Service', shape='rectangle')
dot.node('USER', 'User Management Service', shape='rectangle')
dot.node('AUTH', 'Auth & Auth Session Service', shape='rectangle')
dot.node('MEDIA', 'Media Service', shape='rectangle')
dot.node('DFS', 'Distributed File Storage (DFS)', shape='rectangle')
dot.node('USERNAME', 'Username Management Service', shape='rectangle')
dot.node('DIALOG', 'Dialog Management Service', shape='rectangle')
dot.node('IDGEN', 'ID Generation Service', shape='rectangle')
dot.node('ETCD', 'Service Discovery (Etcd)', shape='rectangle')

# Define nodes for technologies
dot.node('GRPC', 'gRPC Communication', shape='ellipse', style='dashed')
dot.node('KAFKA', 'Kafka', shape='ellipse', style='dashed')
dot.node('REDIS', 'Redis', shape='ellipse', style='dashed')
dot.node('MINIO', 'MinIO', shape='ellipse', style='dashed')
dot.node('MYSQL', 'MySQL', shape='ellipse', style='dashed')

# Define edges for communication
dot.edge('BFF', 'MSG', label='gRPC', dir='forward')
dot.edge('BFF', 'USER', label='gRPC', dir='forward')
dot.edge('BFF', 'CHAT', label='gRPC', dir='forward')
dot.edge('MSG', 'KAFKA', label='Async Ops', dir='forward')
dot.edge('USER', 'REDIS', label='Caching', dir='forward')
dot.edge('AUTH', 'REDIS', label='Caching', dir='forward')
dot.edge('MEDIA', 'DFS', label='File Storage', dir='forward')
dot.edge('MEDIA', 'MINIO', label='Object Storage', dir='forward')
dot.edge('USERNAME', 'MYSQL', label='Data Storage', dir='forward')
dot.edge('DIALOG', 'KAFKA', label='Sync Updates', dir='forward')
dot.edge('IDGEN', 'REDIS', label='ID Generation', dir='forward')
dot.edge('DFS', 'MINIO', label='File Access', dir='forward')
dot.edge('DFS', 'MEDIA', label='Media Access', dir='forward')

# Service Discovery
dot.edge('ETCD', 'BFF', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'MSG', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'CHAT', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'USER', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'AUTH', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'MEDIA', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'USERNAME', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'DIALOG', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'IDGEN', label='Service Discovery', dir='forward')
dot.edge('ETCD', 'DFS', label='Service Discovery', dir='forward')

dot.render('teamgram_server_architecture')
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='E-commerce Microservices Architecture')
dot.attr(rankdir='TB', splines='ortho')

# Global node styling
dot.attr('node', fontname='Arial', fontsize='10', shape='rectangle', style='rounded')

# Add clusters/subgraphs
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Client Layer', style='rounded', color='lightgrey')
    c.node('client', 'External\nClients', shape='box3d')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='API Gateway Layer', style='rounded', color='lightblue')
    c.node('gateway', 'API Gateway\n(Netflix Zuul)\nJWT Auth', color='blue')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Service Layer', style='rounded', color='lightgreen')
    c.node('auth_service', 'Authentication\nService', color='darkgreen')
    c.node('member_service', 'Member Service\n+ Redis Cache', color='darkgreen')
    c.node('order_service', 'Order Service', color='darkgreen')
    c.node('product_service', 'Product Service\n+ Redis Cache', color='darkgreen')

with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Infrastructure Services', style='rounded', color='lightyellow')
    c.node('eureka', 'Eureka Server\nService Discovery', color='orange')
    c.node('config', 'Config Server\nCentralized Config', color='orange')

with dot.subgraph(name='cluster_4') as c:
    c.attr(label='Data Layer', style='rounded', color='pink')
    c.node('mysql', 'MySQL\nPersistence', shape='cylinder', color='red')
    c.node('redis', 'Redis\nCache', shape='cylinder', color='red')
    c.node('kafka', 'Kafka\nMessage Broker', shape='cylinder', color='red')

# Add edges
# Client interactions
dot.edge('client', 'gateway', 'HTTPS')

# Gateway routes
dot.edge('gateway', 'auth_service', 'REST/JWT')
dot.edge('gateway', 'member_service', 'REST')
dot.edge('gateway', 'order_service', 'REST')
dot.edge('gateway', 'product_service', 'REST')

# Service interactions
dot.edge('order_service', 'product_service', 'Feign Client')
dot.edge('member_service', 'redis', 'Cache Operations')
dot.edge('product_service', 'redis', 'Cache Operations')
dot.edge('product_service', 'kafka', 'Inventory Updates')

# Database connections
dot.edge('member_service', 'mysql', 'JPA')
dot.edge('order_service', 'mysql', 'JPA')
dot.edge('product_service', 'mysql', 'JPA')
dot.edge('auth_service', 'mysql', 'JPA')

# Infrastructure connections
dot.edge('auth_service', 'eureka', 'Register/Discover')
dot.edge('member_service', 'eureka', 'Register/Discover')
dot.edge('order_service', 'eureka', 'Register/Discover')
dot.edge('product_service', 'eureka', 'Register/Discover')

dot.edge('auth_service', 'config', 'Get Config')
dot.edge('member_service', 'config', 'Get Config')
dot.edge('order_service', 'config', 'Get Config')
dot.edge('product_service', 'config', 'Get Config')

# Save the diagram
dot.render('ecommerce_architecture', format='png', cleanup=True)
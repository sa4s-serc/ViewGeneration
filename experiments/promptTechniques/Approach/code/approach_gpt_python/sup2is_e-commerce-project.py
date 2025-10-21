from graphviz import Digraph

def generate_architecture_diagram():
    dot = Digraph(comment='E-commerce Platform Architecture', format='png')

    # Microservices as rectangles
    dot.node('API Gateway', 'API Gateway\n(Netflix Zuul)\nHandles routing, auth', shape='rectangle', style='filled', fillcolor='lightblue')
    dot.node('Member Service', 'Member Service\nManages accounts\nSpring Data JPA + Redis', shape='rectangle', style='filled', fillcolor='lightgreen')
    dot.node('Order Service', 'Order Service\nManages orders\nFeign Client', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('Product Service', 'Product Service\nManages catalog\nKafka + Redis', shape='rectangle', style='filled', fillcolor='lightpink')
    dot.node('Auth Service', 'Authentication Service\nHandles JWT\nIssues Tokens', shape='rectangle', style='filled', fillcolor='lightcoral')
    dot.node('Eureka Server', 'Eureka Server\nService Discovery', shape='rectangle', style='filled', fillcolor='lightgrey')
    dot.node('Config Server', 'Config Server\nCentralized Config', shape='rectangle', style='filled', fillcolor='lightcyan')

    # Databases as cylinders
    dot.node('H2 DB', 'H2 Database\n(Dev)', shape='cylinder', style='filled', fillcolor='white')
    dot.node('MySQL DB', 'MySQL Database\n(Int)', shape='cylinder', style='filled', fillcolor='white')
    dot.node('Redis Cache', 'Redis Cache\n(Caching)', shape='cylinder', style='filled', fillcolor='white')

    # Connections
    dot.edge('API Gateway', 'Member Service', label='REST API', arrowhead='vee')
    dot.edge('API Gateway', 'Order Service', label='REST API', arrowhead='vee')
    dot.edge('API Gateway', 'Product Service', label='REST API', arrowhead='vee')
    dot.edge('API Gateway', 'Auth Service', label='REST API', arrowhead='vee')
    dot.edge('Order Service', 'Product Service', label='Feign Client', arrowhead='vee')
    dot.edge('Product Service', 'Kafka', label='Async Updates', style='dashed')
    dot.edge('Auth Service', 'API Gateway', label='JWT Validation', arrowhead='vee')
    dot.edge('Eureka Server', 'API Gateway', label='Service Registry', arrowhead='vee')
    dot.edge('Eureka Server', 'Member Service', label='Service Registry', arrowhead='vee')
    dot.edge('Eureka Server', 'Order Service', label='Service Registry', arrowhead='vee')
    dot.edge('Eureka Server', 'Product Service', label='Service Registry', arrowhead='vee')
    dot.edge('Eureka Server', 'Auth Service', label='Service Registry', arrowhead='vee')
    dot.edge('Member Service', 'H2 DB', label='Data Storage', arrowhead='vee')
    dot.edge('Order Service', 'H2 DB', label='Data Storage', arrowhead='vee')
    dot.edge('Product Service', 'H2 DB', label='Data Storage', arrowhead='vee')
    dot.edge('Member Service', 'MySQL DB', label='Data Storage', arrowhead='vee')
    dot.edge('Order Service', 'MySQL DB', label='Data Storage', arrowhead='vee')
    dot.edge('Product Service', 'MySQL DB', label='Data Storage', arrowhead='vee')
    dot.edge('Member Service', 'Redis Cache', label='Caching', arrowhead='vee')
    dot.edge('Product Service', 'Redis Cache', label='Caching', arrowhead='vee')

    # Render diagram
    dot.render('ecommerce_architecture')

generate_architecture_diagram()
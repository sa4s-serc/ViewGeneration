from graphviz import Digraph

dot = Digraph(comment='MicroServices POC Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add microservices
dot.node('catalog', 'Catalog Service\n(.NET 5.0)')
dot.node('customer', 'Customer Service\n(.NET 5.0)')
dot.node('order', 'Order Service\n(.NET 5.0)')

# Add databases
dot.attr('node', shape='cylinder')
dot.node('catalog_db', 'Catalog\nMongoDB')
dot.node('customer_db', 'Customer\nMongoDB')
dot.node('order_db', 'Order\nMongoDB')

# Add message broker
dot.attr('node', shape='hexagon')
dot.node('rabbitmq', 'RabbitMQ\nMessage Broker')

# Add connections between services and their databases
dot.edge('catalog', 'catalog_db')
dot.edge('customer', 'customer_db')
dot.edge('order', 'order_db')

# Add event-driven communication through RabbitMQ
dot.edge('catalog', 'rabbitmq', 'CatalogItemCreated')
dot.edge('customer', 'rabbitmq', 'CustomerUpdated')
dot.edge('order', 'rabbitmq', 'OrderCreated')
dot.edge('rabbitmq', 'order', 'CatalogItemCreated')
dot.edge('rabbitmq', 'order', 'CustomerUpdated')
dot.edge('rabbitmq', 'customer', 'OrderCreated')

# Add health checks
dot.attr('node', shape='diamond')
dot.node('health', 'Health Checks\nDashboard')
dot.edge('health', 'catalog')
dot.edge('health', 'customer')
dot.edge('health', 'order')
dot.edge('health', 'rabbitmq')

print(dot.source)
dot.render('microservices_architecture', view=True, format='png')
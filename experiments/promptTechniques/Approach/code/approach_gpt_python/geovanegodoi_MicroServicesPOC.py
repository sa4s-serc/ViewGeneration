from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='MicroServicesPOC Architecture', format='png')

# Define styles for different components
styles = {
    'CatalogMicroservice': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightblue'},
    'CustomerMicroservice': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightgreen'},
    'OrderMicroservice': {'shape': 'rectangle', 'style': 'filled', 'fillcolor': 'lightcoral'},
    'Database': {'shape': 'cylinder', 'style': 'filled', 'fillcolor': 'lightgrey'},
    'RabbitMQ': {'shape': 'ellipse', 'style': 'filled', 'fillcolor': 'orange'}
}

# Add nodes for microservices
dot.node('Catalog', 'Catalog Microservice', **styles['CatalogMicroservice'])
dot.node('Customer', 'Customer Microservice', **styles['CustomerMicroservice'])
dot.node('Order', 'Order Microservice', **styles['OrderMicroservice'])

# Add nodes for databases
dot.node('CatalogDB', 'CatalogDB', **styles['Database'])
dot.node('CustomerDB', 'CustomerDB', **styles['Database'])
dot.node('OrderDB', 'OrderDB', **styles['Database'])

# Add node for RabbitMQ
dot.node('RabbitMQ', 'RabbitMQ', **styles['RabbitMQ'])

# Add edges for microservices to their databases
dot.edge('Catalog', 'CatalogDB', label='CRUD')
dot.edge('Customer', 'CustomerDB', label='CRUD')
dot.edge('Order', 'OrderDB', label='CRUD')

# Add edges for event-driven communication via RabbitMQ
dot.edge('Catalog', 'RabbitMQ', label='Publish/Subscribe')
dot.edge('Customer', 'RabbitMQ', label='Publish/Subscribe')
dot.edge('Order', 'RabbitMQ', label='Publish/Subscribe')

# Add bi-directional communication between microservices
dot.edge('Catalog', 'Customer', label='Event: CustomerUpdated', dir='both')
dot.edge('Customer', 'Order', label='Event: OrderCreated', dir='both')
dot.edge('Order', 'Catalog', label='Event: CatalogItemCreated', dir='both')

# Render the graph to a file
dot.render('MicroServicesPOC_Architecture')
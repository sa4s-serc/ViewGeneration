import graphviz

dot = graphviz.Digraph(comment='Microservices Architecture')
dot.attr(rankdir='TB')

with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Catalog Microservice', style='filled', color='lightgrey')
    c.node('catalog_service', 'Catalog Service', shape='rectangle')
    c.node('catalog_db', 'Catalog DB\n(MongoDB)', shape='cylinder')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Customer Microservice', style='filled', color='lightgrey')
    c.node('customer_service', 'Customer Service', shape='rectangle')
    c.node('customer_db', 'Customer DB\n(MongoDB)', shape='cylinder')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Order Microservice', style='filled', color='lightgrey')
    c.node('order_service', 'Order Service', shape='rectangle')
    c.node('order_db', 'Order DB\n(MongoDB)', shape='cylinder')

dot.node('rabbitmq', 'RabbitMQ\nMessage Bus', shape='ellipse', style='filled', color='lightblue')
dot.node('events', 'MSPOC.Events\n(Shared Contracts)', shape='note')

dot.edge('catalog_service', 'rabbitmq', label='publishes\nCatalogItemCreated')
dot.edge('customer_service', 'rabbitmq', label='publishes\nCustomerUpdated')
dot.edge('order_service', 'rabbitmq', label='publishes\nOrderCreated')
dot.edge('rabbitmq', 'customer_service', label='consumes\nOrderCreated, OrderUpdated, OrderRemoved')
dot.edge('rabbitmq', 'order_service', label='consumes\nCatalogItemCreated, CustomerUpdated')

dot.edge('catalog_service', 'catalog_db', style='dashed')
dot.edge('customer_service', 'customer_db', style='dashed')
dot.edge('order_service', 'order_db', style='dashed')

dot.edge('events', 'catalog_service', style='dotted')
dot.edge('events', 'customer_service', style='dotted')
dot.edge('events', 'order_service', style='dotted')

dot.render('microservices_architecture', format='png', cleanup=True)
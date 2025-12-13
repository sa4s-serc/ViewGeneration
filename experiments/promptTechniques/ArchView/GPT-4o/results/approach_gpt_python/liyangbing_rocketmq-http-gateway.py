from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='RocketMQ HTTP Gateway Architecture')

# Define nodes for core components
dot.node('A', 'HTTP Gateway')
dot.node('B', 'Message Produce Request')
dot.node('C', 'ProduceMessageProcessor')
dot.node('D', 'ProducerManager')
dot.node('E', 'RocketMQ Producer')
dot.node('F', 'ConsumerManager')
dot.node('G', 'HttpMessageListenerConcurrently')
dot.node('H', 'HTTP Callback')
dot.node('I', 'SubscriptionChangeWatcher')
dot.node('J', 'Configuration')
dot.node('K', 'Subscription')

# Define edges for communication paths
dot.edge('A', 'B', label='Receive HTTP Request')
dot.edge('B', 'C', label='Decode & Validate')
dot.edge('C', 'D', label='Process Message')
dot.edge('D', 'E', label='Send to RocketMQ')
dot.edge('E', 'F', label='Message Arrival')
dot.edge('F', 'G', label='Manage Consumer Lifecycle')
dot.edge('G', 'H', label='Push to HTTP Endpoint')
dot.edge('I', 'J', label='Update Config')
dot.edge('J', 'K', label='Manage Subscriptions')

# Define styles for the diagram
dot.attr('node', shape='rect', style='filled', color='lightgrey')
dot.attr('edge', arrowhead='vee')

# Render the diagram to a file
dot.render('rocketmq_http_gateway_architecture', format='png', cleanup=True)
from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='RocketMQ HTTP Gateway Architecture')

# Set graph attributes for layout
dot.attr(rankdir='TB', splines='ortho')
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Define node colors
GATEWAY_COLOR = '#ADD8E6'  # Light blue
MESSAGING_COLOR = '#98FB98'  # Light green
MANAGER_COLOR = '#FFE4B5'   # Light orange
CLIENT_COLOR = '#E6E6FA'    # Light purple

# Add main components with colors and descriptions
with dot.subgraph(name='cluster_gateway') as gateway:
    gateway.attr(label='HTTP Gateway Layer', style='rounded', bgcolor=GATEWAY_COLOR)
    gateway.node('transport', 'Transport Layer\n(Netty)\nRequestDecoder\nResponseEncoder')
    gateway.node('processor', 'Processor Layer\nMessageProduceRequest\nProduceMessageProcessor')

with dot.subgraph(name='cluster_management') as management:
    management.attr(label='Management Layer', style='rounded', bgcolor=MANAGER_COLOR)
    management.node('producer_mgr', 'Producer Manager\nLifecycle Management\nIdle Monitoring')
    management.node('consumer_mgr', 'Consumer Manager\nSubscription Management\nCallback Handling')
    management.node('subscription', 'Subscription Manager\nDynamic Configuration\nChange Watcher')

with dot.subgraph(name='cluster_messaging') as messaging:
    messaging.attr(label='Messaging Layer', style='rounded', bgcolor=MESSAGING_COLOR)
    messaging.node('rocketmq', 'RocketMQ\nMessage Queue')

with dot.subgraph(name='cluster_clients') as clients:
    clients.attr(label='Client Layer', style='rounded', bgcolor=CLIENT_COLOR)
    clients.node('http_client', 'HTTP Clients')
    clients.node('http_callback', 'HTTP Callback\nEndpoints')

# Add edges with descriptions
dot.edge('http_client', 'transport', 'HTTP Requests')
dot.edge('transport', 'processor', 'Decoded Requests')
dot.edge('processor', 'producer_mgr', 'Message Production')
dot.edge('producer_mgr', 'rocketmq', 'Send Messages')
dot.edge('rocketmq', 'consumer_mgr', 'Consume Messages')
dot.edge('consumer_mgr', 'http_callback', 'HTTP Callbacks')
dot.edge('subscription', 'producer_mgr', 'Configure Producers')
dot.edge('subscription', 'consumer_mgr', 'Configure Consumers')

# Set title
dot.attr(label='\nRocketMQ HTTP Gateway Architecture\nMessage Flow and Component Interaction', labelloc='t', fontsize='16')

# Save the diagram
dot.render('rocketmq_http_gateway_architecture', format='png', cleanup=True)
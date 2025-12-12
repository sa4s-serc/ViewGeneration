import graphviz

dot = graphviz.Digraph(comment='RocketMQ HTTP Gateway Architecture')
dot.attr(rankdir='TB', size='12,14')

# External components
dot.node('HTTP_Client', 'HTTP Client', shape='ellipse', style='filled', color='lightblue')
dot.node('RocketMQ', 'RocketMQ Cluster', shape='cylinder', style='filled', color='lightcoral')

# Main Gateway container
with dot.subgraph(name='cluster_gateway') as gateway:
    gateway.attr(label='RocketMQ HTTP Gateway', style='filled', color='lightgrey', fontsize='16')
    
    # Transport Layer
    with gateway.subgraph(name='cluster_transport') as transport:
        transport.attr(label='Transport Layer (Netty)', style='filled', color='lightblue')
        transport.node('RequestDecoder', 'Request Decoder')
        transport.node('RequestValidator', 'Request Validator')
        transport.node('ResponseEncoder', 'Response Encoder')
        transport.node('GatewayLogging', 'Gateway Logging Handler')
        transport.node('NettyConnection', 'Netty Connection Manager')
        
    # Processor Layer
    with gateway.subgraph(name='cluster_processor') as processor:
        processor.attr(label='Processor Layer', style='filled', color='lightgreen')
        processor.node('ProduceProcessor', 'ProduceMessage Processor')
        processor.node('ProducerManager', 'Producer Manager')
        processor.node('ConsumerManager', 'Consumer Manager')
        processor.node('HttpMessageListener', 'HttpMessage Listener')
        processor.node('SubscriptionWatcher', 'Subscription Change Watcher')
        
    # Common Layer
    with gateway.subgraph(name='cluster_common') as common:
        common.attr(label='Common Layer', style='filled', color='lightyellow')
        common.node('HttpExecutor', 'Http Executor')
        common.node('ServiceBase', 'Service Base')
        common.node('HttpClients', 'Http Clients Factory')

# External connections
dot.edge('HTTP_Client', 'RequestDecoder', label='HTTP Request', color='blue')
dot.edge('ResponseEncoder', 'HTTP_Client', label='HTTP Response', color='green')

# Transport layer flow
dot.edge('RequestDecoder', 'RequestValidator', label='Decoded Request')
dot.edge('RequestValidator', 'GatewayLogging', label='Validated Request')
dot.edge('GatewayLogging', 'NettyConnection', label='Logged Request')
dot.edge('NettyConnection', 'ProduceProcessor', label='Forward to Processor')

# Message production flow
dot.edge('ProduceProcessor', 'ProducerManager', label='Send Request')
dot.edge('ProducerManager', 'RocketMQ', label='Produce Message', style='dashed', color='red')

# Message consumption flow
dot.edge('RocketMQ', 'HttpMessageListener', label='Consume Message', style='dashed', color='orange')
dot.edge('HttpMessageListener', 'ConsumerManager', label='Message Received')
dot.edge('ConsumerManager', 'HttpExecutor', label='Execute Callback')
dot.edge('HttpExecutor', 'HttpClients', label='Get HTTP Client')
dot.edge('HttpClients', 'HTTP_Client', label='HTTP Callback', style='dotted', color='purple')

# Subscription management
dot.edge('SubscriptionWatcher', 'ProducerManager', label='Update Subscriptions', style='dashed')
dot.edge('SubscriptionWatcher', 'ConsumerManager', label='Update Subscriptions', style='dashed')

# Common infrastructure
dot.edge('ServiceBase', 'ProducerManager', label='Lifecycle', style='dotted')
dot.edge('ServiceBase', 'ConsumerManager', label='Lifecycle', style='dotted')
dot.edge('ServiceBase', 'HttpMessageListener', label='Lifecycle', style='dotted')

# Response flow
dot.edge('ProduceProcessor', 'ResponseEncoder', label='Process Result', color='darkgreen')

dot.render('rocketmq_gateway_architecture', format='png', cleanup=True)
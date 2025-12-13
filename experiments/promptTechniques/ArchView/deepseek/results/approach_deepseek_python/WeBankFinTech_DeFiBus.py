from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Rocketmq
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet

with Diagram("DeFiBus Broker Architecture", show=False, direction="TB"):
    with Cluster("DeFiBus Broker Layer"):
        broker_controller = Server("DeFiBrokerController")
        
        with Cluster("Message Processing"):
            send_processor = Server("DeFiSendMessageProcessor")
            reply_processor = Server("DeFiReplyMessageProcessor")
            pull_processor = Server("DeFiPullMessageProcessor")
            admin_processor = Server("DeFiAdminBrokerProcessor")
        
        with Cluster("Client Management"):
            producer_manager = Server("DeFiProducerManager")
            consumer_manager = Server("DeFiConsumerManager")
        
        with Cluster("Queue Management"):
            queue_manager = Server("ConsumeQueueManager")
            queue_monitor = Server("QueueListeningMonitor")
            adjust_strategy = Server("AdjustQueueNumStrategy")
        
        with Cluster("Security & Control"):
            redirect_manager = Server("MessageRedirectManager")
            access_lock = Server("ConsumeQueueAccessLockManager")
        
        with Cluster("Storage"):
            plugin_store = Redis("DeFiPluginMessageStore")
            topic_config = Redis("DeFiTopicConfigManager")
        
        rebalance_manager = Server("ClientRebalanceResultManager")
        broker2client = Server("DeFiBusBroker2Client")

    with Cluster("Apache RocketMQ Core"):
        rocketmq_core = Rocketmq("RocketMQ Core")
    
    with Cluster("External Clients"):
        producers = Client("Producers")
        consumers = Client("Consumers")

    # Core relationships
    broker_controller >> [
        send_processor, reply_processor, pull_processor, admin_processor,
        producer_manager, consumer_manager, queue_manager, redirect_manager,
        access_lock, plugin_store, topic_config, rebalance_manager, broker2client
    ]
    
    # Message flow
    producers >> send_processor
    send_processor >> queue_manager
    queue_manager >> plugin_store
    plugin_store >> rocketmq_core
    
    # Reply flow
    consumers >> pull_processor
    pull_processor >> queue_manager
    reply_processor >> broker2client >> consumers
    
    # Management flows
    admin_processor >> [topic_config, queue_manager]
    consumer_manager >> [queue_manager, adjust_strategy, rebalance_manager]
    producer_manager >> queue_manager
    
    # Monitoring and control
    queue_monitor >> queue_manager
    adjust_strategy >> queue_manager
    redirect_manager >> [send_processor, pull_processor]
    access_lock >> pull_processor
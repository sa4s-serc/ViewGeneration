from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Kafka
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL

with Diagram("KafkaCap Architecture", show=False):
    user = User("End User")
    
    with Cluster("Capture Devices"):
        aeron = Server("Aeron Capture")
        multicast = Server("Multicast Capture") 
        websocket = Server("Websocket Capture")
    
    with Cluster("Capture Topics"):
        aeron_topic = Kafka("Aeron Topic")
        multicast_topic = Kafka("Multicast Topic")
        websocket_topic = Kafka("Websocket Topic")
    
    with Cluster("Deduplicator"):
        dedup_consumer = Server("Deduplicator Consumer")
        buffered_publisher = Server("Buffered Publisher")
        recovery_service = Server("Recovery Service")
    
    with Cluster("Strategies"):
        dedup_strategy = Server("Dedup Strategy")
        capture_queue = Server("Capture Queue")
        record_populator = Server("Record Populator")
    
    outbound_topic = Kafka("Outbound Topic")
    
    user >> aeron
    user >> multicast
    user >> websocket
    aeron >> aeron_topic
    multicast >> multicast_topic
    websocket >> websocket_topic
    aeron_topic >> dedup_consumer
    multicast_topic >> dedup_consumer
    websocket_topic >> dedup_consumer
    dedup_consumer >> dedup_strategy
    dedup_strategy >> buffered_publisher
    buffered_publisher >> outbound_topic
    recovery_service >> outbound_topic
    capture_queue >> record_populator
    record_populator >> buffered_publisher
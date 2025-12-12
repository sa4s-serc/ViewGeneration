from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.analytics import Kinesis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Rust
from diagrams.aws.general import User

with Diagram("SWIR Sidecar Service Architecture", show=False):
    user = User("Client Application")
    
    with Cluster("SWIR Sidecar"):
        with Cluster("Frontend Handlers"):
            http_handler = Nginx("HTTP Handler")
            grpc_handler = Rust("gRPC Handler")
        
        with Cluster("Core Handlers"):
            si_handlers = Rust("Service Invocation")
            messaging_handlers = Rust("PubSub Messaging")
            persistence_handlers = Rust("Data Persistence")
        
        with Cluster("Support Services"):
            config = Rust("Configuration")
            metrics = Rust("Metrics & Tracing")
            service_discovery = Rust("Service Discovery")
    
    with Cluster("Message Brokers"):
        kafka = Kafka("Kafka")
        nats = Kafka("NATS")
        aws_kinesis = Kinesis("AWS Kinesis")
    
    with Cluster("Persistence Stores"):
        redis = Redis("Redis")
        dynamodb = Dynamodb("DynamoDB")
    
    with Cluster("Backend Services"):
        backend_services = [EC2("Service A"), 
                          EC2("Service B"),
                          EC2("Service C")]
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        opentelemetry = Rust("OpenTelemetry")

    user >> http_handler
    user >> grpc_handler
    http_handler >> si_handlers
    http_handler >> messaging_handlers
    http_handler >> persistence_handlers
    grpc_handler >> si_handlers
    grpc_handler >> messaging_handlers
    grpc_handler >> persistence_handlers
    
    si_handlers >> service_discovery
    service_discovery >> backend_services
    
    messaging_handlers >> kafka
    messaging_handlers >> nats
    messaging_handlers >> aws_kinesis
    
    persistence_handlers >> redis
    persistence_handlers >> dynamodb
    
    config >> si_handlers
    config >> messaging_handlers
    config >> persistence_handlers
    
    si_handlers >> opentelemetry
    messaging_handlers >> opentelemetry
    persistence_handlers >> opentelemetry
    opentelemetry >> prometheus
    prometheus >> grafana
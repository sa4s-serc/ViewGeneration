from diagrams import Diagram, Cluster
from diagrams.programming.language import Go
from diagrams.onprem.queue import Kafka
from diagrams.elastic.elasticsearch import Logstash
from diagrams.onprem.monitoring import Grafana
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.onprem.database import PostgreSQL
from diagrams.aws.mobile import APIGateway

with Diagram("Go-Zero Microservices Architecture", show=False):
    api_gateway = APIGateway("API Gateway")
    service_discovery = Service("Service Discovery")
    load_balancer = Service("Load Balancer")

    with Cluster("Microservices"):
        service1 = Pod("Service 1")
        service2 = Pod("Service 2")
        service3 = Pod("Service 3")

    db = PostgreSQL("Database")
    message_queue = Kafka("Message Queue")
    log_aggregator = Logstash("Log Aggregator")
    monitoring = Grafana("Monitoring")

    api_gateway >> load_balancer >> service_discovery
    service_discovery >> service1
    service_discovery >> service2
    service_discovery >> service3
    service1 >> db
    service2 >> message_queue
    service3 >> message_queue
    service1 >> log_aggregator
    service2 >> log_aggregator
    service3 >> log_aggregator
    log_aggregator >> monitoring
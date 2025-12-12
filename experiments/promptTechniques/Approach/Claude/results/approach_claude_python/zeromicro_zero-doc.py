from diagrams import Diagram, Cluster
from diagrams.programming.framework import FastAPI
from diagrams.onprem.queue import Kafka, RabbitMQ
from diagrams.onprem.database import MySQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.compute import Server

with Diagram("Go-Zero Microservices Architecture", show=False):
    
    with Cluster("API Gateway Layer"):
        gateway = Nginx("API Gateway")

    with Cluster("Service Layer"):
        api = FastAPI("REST API")
        rpc = Server("zRPC Service")

    with Cluster("Message Layer"):
        kafka = Kafka("Event Bus")
        mq = RabbitMQ("Message Queue")

    with Cluster("Data Layer"):
        db = MySQL("MySQL")
        cache = Redis("Cache")

    with Cluster("Monitoring"):
        metrics = Prometheus("Metrics")
        dashboard = Grafana("Dashboard")

    # Connect components
    gateway >> api
    gateway >> rpc
    
    api >> kafka
    api >> mq
    rpc >> kafka
    rpc >> mq
    
    api >> cache
    api >> db
    rpc >> cache
    rpc >> db
    
    api >> metrics
    rpc >> metrics
    metrics >> dashboard
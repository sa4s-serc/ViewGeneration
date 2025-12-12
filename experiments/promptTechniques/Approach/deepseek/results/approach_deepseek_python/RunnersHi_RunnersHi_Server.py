from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Spring
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger

with Diagram("Microservices Architecture", show=False, direction="LR"):
    load_balancer = Nginx("Load Balancer")
    
    with Cluster("Application Layer"):
        api_gateway = Spring("API Gateway")
        
        with Cluster("Microservices"):
            user_service = Spring("User Service")
            order_service = Spring("Order Service")
            payment_service = Spring("Payment Service")
            inventory_service = Spring("Inventory Service")
        
        api_gateway >> [user_service, order_service, payment_service, inventory_service]
    
    with Cluster("Data Layer"):
        with Cluster("Primary Database"):
            mysql = MySQL("MySQL")
        
        with Cluster("Cache"):
            redis = Redis("Redis")
        
        with Cluster("Message Queue"):
            rabbitmq = Docker("RabbitMQ")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        loki = Loki("Loki")
        jaeger = Jaeger("Jaeger")
    
    load_balancer >> api_gateway
    user_service >> mysql
    order_service >> mysql
    payment_service >> mysql
    inventory_service >> mysql
    user_service >> redis
    order_service >> redis
    payment_service >> redis
    inventory_service >> redis
    order_service >> rabbitmq
    payment_service >> rabbitmq
    
    [user_service, order_service, payment_service, inventory_service] >> prometheus
    [user_service, order_service, payment_service, inventory_service] >> loki
    [user_service, order_service, payment_service, inventory_service] >> jaeger
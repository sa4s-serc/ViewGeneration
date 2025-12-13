from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki

with Diagram("System Architecture", show=False):
    with Cluster("Web Tier"):
        nginx = Nginx("Nginx")
        
    with Cluster("Application Tier"):
        with Cluster("Microservices"):
            api_gateway = Docker("API Gateway")
            user_service = Docker("User Service")
            order_service = Docker("Order Service")
            
    with Cluster("Data Tier"):
        redis = Redis("Redis Cache")
        postgres = Postgresql("PostgreSQL")
        
    with Cluster("Monitoring"):
        grafana = Grafana("Grafana")
        prometheus = Prometheus("Prometheus")
        loki = Loki("Loki")
        
    with Cluster("CI/CD"):
        jenkins = Jenkins("Jenkins")
    
    nginx >> api_gateway
    api_gateway >> user_service
    api_gateway >> order_service
    user_service >> redis
    user_service >> postgres
    order_service >> redis
    order_service >> postgres
    user_service >> prometheus
    order_service >> prometheus
    prometheus >> grafana
    loki >> grafana
    jenkins >> api_gateway
    jenkins >> user_service
    jenkins >> order_service
from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.onprem.network import Internet
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.logging import Loki

with Diagram("System Architecture", show=False, direction="TB"):
    user = User("End User")
    internet = Internet("Internet")
    
    with Diagram("Application Layer"):
        web_server = Server("Web Server")
        app_server = Server("Application Server")
        api_gateway = Server("API Gateway")
        
    with Diagram("Data Layer"):
        primary_db = Mongodb("Primary Database")
        cache = Redis("Cache")
        message_queue = Kafka("Message Queue")
        
    with Diagram("Monitoring Layer"):
        metrics = Prometheus("Metrics")
        logs = Loki("Logs")
        dashboard = Grafana("Dashboard")
    
    user >> internet >> api_gateway
    api_gateway >> web_server >> app_server
    app_server >> primary_db
    app_server >> cache
    app_server >> message_queue
    
    web_server >> metrics
    app_server >> metrics
    primary_db >> metrics
    
    web_server >> logs
    app_server >> logs
    primary_db >> logs
    
    metrics >> dashboard
    logs >> dashboard
from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki

with Diagram("System Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Web Layer"):
        lb = Nginx("Load Balancer")
        web_servers = [Server("Web Server 1"),
                      Server("Web Server 2"),
                      Server("Web Server 3")]
    
    with Cluster("Application Layer"):
        app_servers = [Server("App Server 1"),
                      Server("App Server 2")]
    
    with Cluster("Data Layer"):
        with Cluster("Primary Database"):
            primary_db = PostgreSQL("PostgreSQL")
            read_replicas = [PostgreSQL("Read Replica 1"),
                           PostgreSQL("Read Replica 2")]
        
        with Cluster("Caching"):
            cache = Redis("Redis Cache")
        
        with Cluster("Message Queue"):
            message_queue = Kafka("Kafka")
    
    with Cluster("Monitoring"):
        monitoring = [Prometheus("Prometheus"),
                     Grafana("Grafana"),
                     Loki("Loki")]
    
    user >> lb
    lb >> web_servers[0]
    lb >> web_servers[1]
    lb >> web_servers[2]
    
    for web_server in web_servers:
        for app_server in app_servers:
            web_server >> app_server
    
    for app_server in app_servers:
        app_server >> primary_db
        app_server >> read_replicas[0]
        app_server >> read_replicas[1]
        app_server >> cache
        app_server >> message_queue
    
    for web_server in web_servers:
        for mon in monitoring:
            web_server >> mon
    
    for app_server in app_servers:
        for mon in monitoring:
            app_server >> mon
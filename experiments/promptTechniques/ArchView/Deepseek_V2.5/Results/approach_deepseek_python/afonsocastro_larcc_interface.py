from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki

with Diagram("System Architecture View", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Web Layer"):
        lb = Nginx("Load Balancer")
        web_server1 = Server("Web Server 1")
        web_server2 = Server("Web Server 2")
    
    with Cluster("Application Layer"):
        app_server1 = Server("App Server 1")
        app_server2 = Server("App Server 2")
    
    with Cluster("Data Layer"):
        with Cluster("Primary Database"):
            primary_db = PostgreSQL("PostgreSQL")
            read_replica1 = PostgreSQL("Read Replica 1")
            read_replica2 = PostgreSQL("Read Replica 2")
        
        with Cluster("Caching"):
            cache = Redis("Redis Cache")
        
        with Cluster("Message Queue"):
            message_queue = Kafka("Kafka")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        loki = Loki("Loki")
    
    user >> lb
    lb >> web_server1
    lb >> web_server2
    web_server1 >> app_server1
    web_server1 >> app_server2
    web_server2 >> app_server1
    web_server2 >> app_server2
    app_server1 >> primary_db
    app_server1 >> read_replica1
    app_server1 >> read_replica2
    app_server1 >> cache
    app_server1 >> message_queue
    app_server2 >> primary_db
    app_server2 >> read_replica1
    app_server2 >> read_replica2
    app_server2 >> cache
    app_server2 >> message_queue
    
    web_server1 >> prometheus
    web_server2 >> prometheus
    app_server1 >> prometheus
    app_server2 >> prometheus
    primary_db >> prometheus
    cache >> prometheus
    
    prometheus >> grafana
    loki >> grafana
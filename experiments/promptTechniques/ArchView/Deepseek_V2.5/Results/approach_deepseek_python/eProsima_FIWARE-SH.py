from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git

with Diagram("System Architecture", show=False, direction="LR"):
    user = User("End User")
    
    with Cluster("Web Tier"):
        lb = Nginx("Load Balancer")
        with Cluster("Application Servers"):
            app_servers = [Server("App Server 1"),
                          Server("App Server 2"),
                          Server("App Server 3")]
    
    with Cluster("Data Tier"):
        with Cluster("Database Cluster"):
            db_primary = PostgreSQL("Primary DB")
            db_replica = PostgreSQL("Replica DB")
        
        cache = Redis("Cache")
        queue = Kafka("Message Queue")
    
    with Cluster("Monitoring"):
        metrics = Prometheus("Metrics")
        logs = Loki("Logs")
        dashboard = Grafana("Dashboard")
    
    with Cluster("CI/CD"):
        ci = Jenkins("CI Server")
        vcs = Git("Version Control")
        registry = Docker("Container Registry")
    
    user >> lb >> app_servers
    app_servers >> db_primary
    app_servers >> db_replica
    app_servers >> cache
    app_servers >> queue
    app_servers >> metrics
    app_servers >> logs
    metrics >> dashboard
    logs >> dashboard
    vcs >> ci >> registry
from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Flask
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Hadoop
from diagrams.onprem.queue import Celery
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki

with Diagram("Microservices Architecture", show=False, direction="LR"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        lb = Nginx("Load Balancer")
        frontend = Flask("Web Application")
        
    with Cluster("Application Layer"):
        with Cluster("Microservices"):
            svc_a = Server("Service A")
            svc_b = Server("Service B")
            svc_c = Server("Service C")
            
    with Cluster("Data Layer"):
        cache = Redis("Cache")
        db = PostgreSQL("Database")
        data_lake = Hadoop("Data Lake")
        
    with Cluster("Monitoring"):
        metrics = Grafana("Metrics")
        logs = Loki("Logs")
        
    with Cluster("Async Processing"):
        queue = Celery("Message Queue")
        worker = Server("Worker")
        
    user >> lb >> frontend
    frontend >> svc_a
    frontend >> svc_b
    frontend >> svc_c
    
    svc_a >> cache
    svc_b >> db
    svc_c >> data_lake
    
    svc_a >> queue
    queue >> worker
    worker >> db
    
    svc_a >> metrics
    svc_b >> logs
    svc_c >> metrics
from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.programming.framework import Spring

with Diagram("URL Shortener Service Architecture", show=False, direction="LR"):
    client = Docker("Client")
    
    with Cluster("Load Balancer"):
        lb = Nginx("Nginx")
    
    with Cluster("Application Layer"):
        app1 = Spring("Spring Boot App 1")
        app2 = Spring("Spring Boot App 2")
    
    with Cluster("Data Layer"):
        cache = Redis("Redis Cache")
        db = MongoDB("MongoDB")
    
    client >> lb
    lb >> app1
    lb >> app2
    app1 >> cache
    app2 >> cache
    cache >> db
    app1 >> db
    app2 >> db
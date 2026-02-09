from diagrams import Diagram, Cluster
from diagrams.programming.framework import Spring
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Java
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Master
from diagrams.k8s.network import Service

with Diagram("Cloud Native Weather Service Architecture", show=False):
    with Cluster("Kubernetes Cluster"):
        master = Master("Control Plane")
        
        with Cluster("Application Pods"):
            pods = [
                Pod("Weather Service"),
                Pod("Health Check"),
                Pod("Metrics")
            ]
            
        svc = Service("LoadBalancer")
        
        with Cluster("Components"):
            app = Spring("JavaEE App")
            db = PostgreSQL("Weather Data")
            java = Java("Payara Micro")
            
        with Cluster("Infrastructure"):
            docker = Docker("Container Runtime")
            nginx = Nginx("Reverse Proxy")
            server = Server("Host")
            
    # Connect components
    svc >> pods
    pods >> app
    app >> java
    app >> db
    master >> pods
    docker >> pods
    nginx >> svc
    server >> docker
from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.gcp.compute import KubernetesEngine
from diagrams.onprem.database import MongoDB
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.framework import Nextjs, Flask
from diagrams.programming.language import Nodejs
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.certificates import CertManager
from diagrams.onprem.network import Nginx

with Diagram("Roof Detection and Geospatial Application Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Kubernetes Cluster (GCP)"):
        with Cluster("Frontend"):
            frontend = Nextjs("Next.js Frontend")
        
        with Cluster("Backend Services"):
            with Cluster("API Layer"):
                api = Flask("Python Flask API")
            
            with Cluster("Metrics Service"):
                metrics = Nodejs("Metrics API")
            
            with Cluster("Message Queue"):
                rabbitmq = RabbitMQ("RabbitMQ")
            
            with Cluster("Database"):
                mongodb = MongoDB("MongoDB")
            
            with Cluster("Monitoring"):
                grafana = Grafana("Grafana")
            
            with Cluster("Certificate Management"):
                cert_manager = CertManager("cert-manager")
            
            with Cluster("Ingress"):
                ingress = Nginx("Nginx Ingress")
    
    user >> ingress
    ingress >> frontend
    frontend >> api
    api >> mongodb
    api >> rabbitmq
    rabbitmq >> metrics
    metrics >> mongodb
    metrics >> grafana
    cert_manager >> ingress
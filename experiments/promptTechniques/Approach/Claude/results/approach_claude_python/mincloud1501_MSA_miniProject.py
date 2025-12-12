from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.k8s.infra import Master
from diagrams.k8s.ecosystem import Helm
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Istio

with Diagram("MSA MiniProject Architecture", show=False):
    with Cluster("Kubernetes Cluster"):
        master = Master("Control Plane")
        
        with Cluster("Deployment Pipeline"):
            docker = Docker("Docker Image")
            helm = Helm("Helm Charts")
        
        with Cluster("Application Tier"):
            deploy = Deployment("Nginx Deployment")
            pods = [Pod("Pod 1"), Pod("Pod 2")]
            svc = Service("LoadBalancer")
            nginx = Nginx("Nginx Server")
        
        with Cluster("Service Mesh & Monitoring"):
            istio = Istio("Service Mesh")
            prom = Prometheus("Monitoring")

        # Define relationships
        docker >> helm >> deploy
        deploy >> pods
        pods >> nginx
        svc >> pods
        master >> deploy
        istio >> pods
        prom >> pods
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.workload import Deployment
from diagrams.k8s.group import Namespace
from diagrams.onprem.client import User
from diagrams.onprem.network import Istio
from diagrams.onprem.container import Docker

with Diagram("Microservices Architecture with Kubernetes and Istio", show=False):
    user = User("Client")

    with Cluster("Kubernetes Cluster"):
        istio = Istio("Istio Service Mesh")

        with Cluster("Nginx Deployment"):
            nginx_deployment = Deployment("Deployment")
            nginx_pod = Pod("Nginx Pod")
            service = Service("Nginx Service")

            nginx_deployment >> nginx_pod
            nginx_pod >> service
            service >> istio

    docker = Docker("Docker Image")
    user >> istio >> nginx_deployment
    docker >> nginx_deployment
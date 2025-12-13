from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.rbac import Role, RoleBinding
from diagrams.onprem.network import Istio
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB

with Diagram("Microservices Architecture on Kubernetes", show=False):
    api = APIServer("Kubernetes API Server")
    
    with Cluster("Kubernetes Cluster"):
        with Cluster("Nginx Deployment"):
            nginx_deployment = Deployment("Nginx Deployment")
            nginx_pods = [Pod("Nginx Pod 1"),
                          Pod("Nginx Pod 2"),
                          Pod("Nginx Pod 3")]
        
        svc = Service("Nginx Service")

        nginx_deployment >> Edge(label="manages") >> nginx_pods
        nginx_pods >> Edge(label="exposes") >> svc
    
    role = Role("RBAC Role")
    role_binding = RoleBinding("RBAC RoleBinding")
    role >> role_binding >> api

    svc >> Edge(label="balanced by") >> ELB("External Load Balancer")
    istio = Istio("Istio Service Mesh")
    istio >> Edge(label="manages traffic") >> svc

    ec2_instances = [EC2("EC2 Instance 1"),
                     EC2("EC2 Instance 2"),
                     EC2("EC2 Instance 3")]
    
    elb = ELB("Elastic Load Balancer")
    svc >> elb >> ec2_instances
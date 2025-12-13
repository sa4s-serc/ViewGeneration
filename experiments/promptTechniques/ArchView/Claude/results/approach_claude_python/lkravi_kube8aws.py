from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, InternetGateway, NLB
from diagrams.aws.security import ACM
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Ansible, Terraform
from diagrams.k8s.compute import Pod
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.infra import Master

with Diagram("Terraform-Ansible Kubernetes Deployment", show=False):
    with Cluster("AWS VPC"):
        igw = InternetGateway("Internet Gateway")
        
        with Cluster("Public Subnet"):
            bastion = EC2("Bastion Host")
            nlb = NLB("Network Load Balancer")

        with Cluster("Private Subnet"):
            with Cluster("Kubernetes Cluster"):
                master = Master("Control Plane")
                api = APIServer("API Server")
                worker1 = Pod("Worker Node 1")
                worker2 = Pod("Worker Node 2")
                worker3 = Pod("Worker Node 3")
                
                master >> api
                api >> [worker1, worker2, worker3]

        # Infrastructure Provisioning Tools
        terraform = Terraform("Infrastructure")
        ansible = Ansible("Configuration")
        docker = Docker("Container Runtime")

        # Connections
        igw >> bastion
        bastion >> master
        nlb >> api
        terraform >> bastion
        terraform >> master
        terraform >> worker1
        terraform >> worker2
        terraform >> worker3
        bastion >> ansible
        ansible >> master
        ansible >> worker1
        ansible >> worker2
        ansible >> worker3
        docker >> worker1
        docker >> worker2
        docker >> worker3
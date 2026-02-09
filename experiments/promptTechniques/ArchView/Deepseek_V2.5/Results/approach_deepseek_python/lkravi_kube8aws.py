from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, VPC, InternetGateway
from diagrams.aws.security import IAM
from diagrams.onprem.iac import Ansible
from diagrams.onprem.container import Docker

with Diagram("Kubernetes Cluster on AWS", show=False, direction="TB"):
    internet = InternetGateway("Internet")
    
    with Cluster("VPC"):
        with Cluster("Public Subnet"):
            bastion = EC2("Bastion Host")
            nlb = ELB("Network Load Balancer")
        
        with Cluster("Private Subnet"):
            master1 = EC2("Master Node 1")
            master2 = EC2("Master Node 2")
            worker1 = EC2("Worker Node 1")
            worker2 = EC2("Worker Node 2")
            worker3 = EC2("Worker Node 3")
    
    ansible = Ansible("Ansible Control")
    docker = Docker("Docker Runtime")
    iam = IAM("IAM Roles")
    
    internet >> nlb
    internet >> bastion
    bastion >> ansible
    ansible >> master1
    ansible >> master2
    ansible >> worker1
    ansible >> worker2
    ansible >> worker3
    nlb >> master1
    nlb >> master2
    master1 >> worker1
    master1 >> worker2
    master1 >> worker3
    master2 >> worker1
    master2 >> worker2
    master2 >> worker3
    docker >> master1
    docker >> master2
    docker >> worker1
    docker >> worker2
    docker >> worker3
    iam >> bastion
    iam >> master1
    iam >> master2
    iam >> worker1
    iam >> worker2
    iam >> worker3
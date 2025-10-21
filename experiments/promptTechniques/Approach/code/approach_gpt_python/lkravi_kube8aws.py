from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import NLB
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.iac import Terraform
from diagrams.onprem.iac import Ansible

with Diagram("Kubernetes Cluster on AWS", show=False, direction="TB"):

    terraform = Terraform("Terraform")
    ansible = Ansible("Ansible")

    with Cluster("AWS Infrastructure"):
        with Cluster("VPC"):
            with Cluster("Subnets"):
                bastion = EC2("Bastion Host")
                masters = [EC2("Master Node 1"),
                           EC2("Master Node 2"),
                           EC2("Master Node 3")]
                workers = [EC2("Worker Node 1"),
                           EC2("Worker Node 2"),
                           EC2("Worker Node 3")]
                nlb = NLB("Network Load Balancer")

            bastion - Edge(label="SSH Access") - masters
            bastion - Edge(label="SSH Access") - workers
            nlb >> Edge(label="API Requests") >> masters

    terraform >> Edge(label="Provision Infrastructure") >> bastion
    terraform >> Edge(label="Setup NLB") >> nlb

    with Cluster("Kubernetes Setup"):
        ansible >> Edge(label="Configure Kubernetes") >> masters
        ansible >> Edge(label="Configure Kubernetes") >> workers

    with Cluster("Monitoring & Management"):
        monitoring = Cloudwatch("CloudWatch")
        monitoring >> Edge(label="Monitor") >> masters
        monitoring >> Edge(label="Monitor") >> workers
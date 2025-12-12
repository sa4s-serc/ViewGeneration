from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Github

with Diagram("Edge Insights for Vision Architecture", show=False):
    with Cluster("Installation & Setup"):
        install = Python("eiv_install.sh")
        setup = Python("eiv_setup.py")
        callbacks = Python("eiv_callbacks.sh")

    with Cluster("Core Components"):
        docker = Docker("Docker Container")
        github = Github("Repository")
        
    with Cluster("Storage & Dependencies"):
        s3 = S3("OpenVINO Models")
        rds = RDS("Configuration DB")

    with Cluster("Runtime"):
        elb = ELB("Load Balancer")
        containers = ECS("OpenVINO Apps")

    # Define relationships
    install >> setup >> callbacks
    github >> docker
    docker >> containers
    s3 >> containers
    rds >> containers
    elb >> containers
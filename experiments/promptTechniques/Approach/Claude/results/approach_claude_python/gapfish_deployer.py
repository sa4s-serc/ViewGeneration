from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import Route53, ELB
from diagrams.k8s.compute import Deploy, Pod
from diagrams.k8s.network import Service
from diagrams.k8s.storage import PV
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions

with Diagram("Gapfish Deployer Architecture", show=False):
    with Cluster("CI/CD Pipeline"):
        github = Github("GitHub Repo")
        actions = GithubActions("GitHub Actions")
        github >> actions

    with Cluster("Kubernetes Cluster"):
        with Cluster("Deployment Components"):
            deploy = Deploy("Deployment")
            pods = [Pod("Pod 1"), Pod("Pod 2")]
            svc = Service("Service")
            pv = PV("ConfigMap/Secrets")
            
            deploy >> pods
            pods >> svc
            pods << pv

    with Cluster("Infrastructure"):
        dns = Route53("DNS")
        lb = ELB("Load Balancer")
        db = RDS("Database")

        actions >> deploy
        dns >> lb
        lb >> svc
        pods >> db
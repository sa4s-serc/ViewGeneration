from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.group import Namespace
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.programming.language import Ruby
from diagrams.generic.compute import Rack

with Diagram("Gapfish Deployer Architecture", show=False):
    cli_user = Users("depctl CLI User")
    github_repo = Github("GitHub Repository")
    codeship_ci = Server("CI/CD Server")

    with Cluster("Kubernetes Cluster"):
        namespace = Namespace("gapfish-namespace")
        deployer = Pod("Deployer")
        service = Service("K8s Service")
        event_logger = Pod("Event Stream Logger")

    env_vars = Docker(".env Files")
    docker_img = Docker("Deployer Docker Image")
    plugins = Rack("Plugins")
    config_management = Ruby("Configuration Management")

    cli_user >> Edge(label="triggers") >> deployer
    deployer >> Edge(label="fetches code") >> github_repo
    deployer >> Edge(label="builds & deploys") >> docker_img
    deployer >> Edge(label="modifies resources") >> service
    deployer >> Edge(label="logs events") >> event_logger
    deployer >> Edge(label="extends functionality") >> plugins
    deployer >> Edge(label="reads config") >> config_management

    codeship_ci >> Edge(label="integrates") >> deployer
    env_vars >> Edge(label="provides config") >> deployer
    event_logger >> Edge(label="notifies") >> plugins

    github_repo >> Edge(label="triggers build") >> codeship_ci
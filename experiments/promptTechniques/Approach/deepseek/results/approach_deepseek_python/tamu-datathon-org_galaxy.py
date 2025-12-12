from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Git
from diagrams.aws.general import User
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Galaxy Repository Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Cluster("TAMU Datathon"):
        with Cluster("Galaxy Repository"):
            router = Nginx("Router")
            docker_compose = Docker("Docker Compose")
            github_actions = GithubActions("GitHub Actions")
            git = Git("Git Submodules")
            
        with Cluster("Backend Services"):
            gatekeeper = EC2("Gatekeeper")
            obos = EC2("OBOS")
            gigabowser = EC2("Gigabowser")
            
        with Cluster("Deployment"):
            heroku = CloudFront("Heroku")
            
    user >> router
    router >> gatekeeper
    router >> obos
    router >> gigabowser
    docker_compose >> router
    github_actions >> heroku
    git >> gatekeeper
    heroku >> gatekeeper
    heroku >> obos
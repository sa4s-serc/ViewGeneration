from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.programming.language import Java
from diagrams.onprem.container import Docker
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.group import Namespace
from diagrams.onprem.ci import GithubActions

with Diagram("Cloud-Native Weather Service Architecture", direction="TB"):

    user = User("Client")

    with Cluster("Kubernetes Cluster"):
        with Cluster("Namespace: WeatherApp"):
            app = Pod("PayaraMicroWeatherService")
            db = PostgreSQL("WeatherDB")
            svc = Service("WeatherService")

        with Cluster("Namespace: Monitoring"):
            health = Pod("Health Checks")
            metrics = Pod("Metrics")
        
        app >> Edge(label="connects to") >> db
        app >> Edge(label="exposes") >> svc
        svc >> Edge(label="REST API") >> user

    with Cluster("CI/CD Pipeline"):
        github = GithubActions("GitHub Actions")
        docker = Docker("Docker Image")
        kubernetes = Namespace("K8s Deployment")

    github >> Edge(label="builds") >> docker >> Edge(label="deploys to") >> kubernetes

    ext_api = Internet("OpenWeatherMap API")
    app >> Edge(label="fetches data from") >> ext_api

    user >> Edge(label="requests data") >> svc
    svc >> Edge(label="responds with data") >> user

    svc >> Edge(label="health checks") >> health
    svc >> Edge(label="provides metrics") >> metrics
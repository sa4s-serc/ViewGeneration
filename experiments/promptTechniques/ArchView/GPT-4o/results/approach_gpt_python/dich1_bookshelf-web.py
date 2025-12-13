from diagrams import Diagram, Cluster
from diagrams.programming.framework import Rails
from diagrams.onprem.client import Client
from diagrams.onprem.database import MySQL
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Git
from diagrams.onprem.ci import CircleCI
from diagrams.onprem.container import Docker

with Diagram("Bookshelf Web Application Architecture", show=True):
    client = Client("User")

    with Cluster("Web Application"):
        frontend = Rails("Front-end")
        backend = Rails("Back-end")

    client >> frontend

    with Cluster("Deployment & CI/CD"):
        git = Git("Source Code")
        circleci = CircleCI("CI/CD Pipeline")
        docker = Docker("Docker & Compose")

    git >> circleci >> docker

    with Cluster("Containerized Services"):
        web_service = Nginx("Web Service")
        app_server = Server("Application Server")
        db = MySQL("Database")

    docker >> web_service >> app_server >> db
    frontend >> backend >> db
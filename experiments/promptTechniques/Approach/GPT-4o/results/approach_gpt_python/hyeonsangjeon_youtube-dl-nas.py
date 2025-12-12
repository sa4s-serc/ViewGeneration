from diagrams import Diagram, Cluster, Edge
from diagrams.programming.flowchart import Action
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Celery
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Git
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.iac import Ansible
from diagrams.onprem.security import Vault

with Diagram("YouTube-dl NAS Architecture", show=False, direction="LR"):
    user = Users("Authenticated User")

    with Cluster("Containerized Web Server"):
        web_server = Server("youtube-dl-server.py")
        api = Action("REST API")
        websocket = Action("WebSocket")
        queue_manager = Celery("Download Queue")
        worker = Action("Download Worker")
        auth = Vault("Basic Auth")
        
        user >> Edge(label="Login/Requests") >> web_server
        web_server >> Edge(label="Authenticate", style="dashed") >> auth
        auth >> Edge(label="Allow") >> web_server
        web_server >> Edge(label="Submit/Manage") >> api
        web_server >> Edge(label="Update", style="dotted") >> websocket
        api >> Edge(label="Queue") >> queue_manager
        queue_manager >> worker

    with Cluster("External Systems"):
        downloader = Git("yt-dlp/youtube-dl")
        container = Docker("Dockerized Application")
        scheduler = Ansible("Daily Updates")
        config = Vault("Auth.json")

        worker >> Edge(label="Download") >> downloader
        container >> Edge(label="Run") >> web_server
        scheduler >> Edge(label="Automatic Update") >> downloader
        config >> Edge(label="Access Credentials") >> web_server

    monitoring = Grafana("Real-time Monitoring")
    websocket >> Edge(label="Progress Updates") >> monitoring
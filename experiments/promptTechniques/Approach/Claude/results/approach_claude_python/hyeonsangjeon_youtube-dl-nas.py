from diagrams import Diagram, Cluster
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Flask
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.onprem.queue import Celery
from diagrams.onprem.network import Traefik

with Diagram("Youtube-DL-NAS Architecture", show=False):
    with Cluster("Docker Container"):
        web = Flask("Web Server")
        worker = Celery("Download Worker")
        queue = RabbitMQ("Queue")
        auth = Python("Auth Service")
        proxy = Traefik("Reverse Proxy")
        
        # Frontend flow
        users = Users("Users")
        users >> proxy >> web
        
        # Authentication flow
        web >> auth
        
        # Download flow
        web >> queue >> worker
        
        # Storage
        storage = Server("NAS Storage")
        worker >> storage
        
        # Real-time updates
        worker >> web
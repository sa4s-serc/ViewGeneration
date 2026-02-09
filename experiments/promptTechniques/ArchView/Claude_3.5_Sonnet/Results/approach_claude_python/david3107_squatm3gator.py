from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flask
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.aws.storage import S3
from diagrams.firebase.develop import Authentication
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS

with Diagram("SquatM3gator Architecture", show=False):
    with Cluster("Frontend"):
        ui = Flask("Web UI")
        
    with Cluster("Backend Services"):
        lb = Nginx("Load Balancer")
        
        with Cluster("Application Layer"):
            api = Server("Flask API")
            auth = Authentication("Auth Service") 
            iam = IAM("Access Control")

        with Cluster("Processing Layer"):
            queue = Redis("Redis Queue")
            worker = Server("Worker")

        with Cluster("Storage Layer"):
            redis_cache = Redis("Redis Cache")
            storage = S3("Domain Results")

    # Frontend to Backend
    ui >> lb >> api

    # API Authentication flow  
    api >> auth
    api >> iam

    # Processing flow
    api >> queue >> worker
    worker >> storage
    worker >> redis_cache

    # Data access
    api >> redis_cache
    api >> storage
from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Celery
from diagrams.onprem.monitoring import Grafana
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana
from diagrams.programming.framework import Flask, React
from diagrams.aws.security import ACM
from diagrams.onprem.aggregator import Fluentd

with Diagram("Arclytics SimCCT Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend"):
        frontend = React("React Client")
    
    with Cluster("Backend Services"):
        with Cluster("SimCCT Service"):
            flask_app = Flask("Flask API")
            auth_service = Server("Auth Service")
            simulation_service = Server("Simulation Service")
            user_service = Server("User Management")
        
        with Cluster("Async Processing"):
            celery = Celery("Celery Worker")
            redis_queue = Redis("Redis Queue")
        
        with Cluster("Data Layer"):
            mongodb = MongoDB("MongoDB")
            redis_cache = Redis("Redis Cache")
    
    with Cluster("Monitoring & Logging"):
        fluentd = Fluentd("Fluentd")
        elasticsearch = Elasticsearch("Elasticsearch")
        kibana = Kibana("Kibana")
        apm = ACM("Elastic APM")
        grafana = Grafana("Grafana")
    
    user >> frontend
    frontend >> flask_app
    flask_app >> auth_service
    flask_app >> simulation_service
    flask_app >> user_service
    flask_app >> redis_cache
    flask_app >> mongodb
    flask_app >> celery
    celery >> redis_queue
    celery >> mongodb
    flask_app >> fluentd
    fluentd >> elasticsearch
    elasticsearch >> kibana
    flask_app >> apm
    apm >> grafana
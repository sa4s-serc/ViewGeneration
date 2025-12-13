from diagrams import Diagram, Cluster
from diagrams.onprem.network import Gunicorn, Zookeeper
from diagrams.onprem.database import MongoDB
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Celery
from diagrams.programming.framework import Flask

with Diagram("MLAB Dashboard and Worker Service Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Dashboard Service"):
        flask_app = Flask("Flask Dashboard")
        gunicorn = Gunicorn("Gunicorn WSGI")
        dashboard_db = MongoDB("MongoDB")
        zk_dashboard = Zookeeper("ZooKeeper")
        
        flask_app >> gunicorn
        flask_app >> dashboard_db
        flask_app >> zk_dashboard
    
    with Cluster("Worker Service"):
        worker_server = Gunicorn("Worker Service")
        model_repo = MongoDB("Model Storage")
        zk_worker = Zookeeper("ZooKeeper")
        celery_worker = Celery("Celery Worker")
        
        worker_server >> model_repo
        worker_server >> zk_worker
        worker_server >> celery_worker
    
    with Cluster("External Services"):
        docker = Docker("Docker Container")
        redis_cache = Redis("Redis Cache")
    
    user >> flask_app
    user >> worker_server
    flask_app >> worker_server
    zk_dashboard >> zk_worker
    dashboard_db >> model_repo
    worker_server >> docker
    worker_server >> redis_cache
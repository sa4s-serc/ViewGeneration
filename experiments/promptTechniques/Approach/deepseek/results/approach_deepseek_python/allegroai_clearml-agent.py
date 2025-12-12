from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Celery
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python

with Diagram("ClearML Agent Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("ClearML Platform"):
        ui = Server("ClearML UI")
        server = Server("ClearML Server")
        queues = Celery("Task Queues")
    
    with Cluster("ClearML Agent"):
        agent = Server("ClearML Agent")
        
        with Cluster("Core Components"):
            resource_monitor = Prometheus("ResourceMonitor")
            req_manager = Python("RequirementsManager")
            docker_int = Docker("Docker Integration")
        
        with Cluster("Integrations"):
            k8s = Server("K8s Integration")
            slurm = Server("SLURM Integration")
    
    with Cluster("Execution Environments"):
        venv = Python("Virtual Env")
        conda = Python("Conda")
        poetry = Python("Poetry")
        docker_env = Docker("Docker Container")
    
    with Cluster("External Systems"):
        k8s_cluster = Server("Kubernetes")
        slurm_cluster = Server("SLURM Cluster")
        storage = PostgreSQL("Storage")
        cache = Redis("Cache")
    
    # Connections
    user >> ui
    ui >> server
    server >> queues
    queues >> agent
    
    agent >> resource_monitor
    agent >> req_manager
    agent >> docker_int
    
    req_manager >> venv
    req_manager >> conda
    req_manager >> poetry
    req_manager >> docker_env
    
    agent >> k8s
    agent >> slurm
    k8s >> k8s_cluster
    slurm >> slurm_cluster
    
    agent >> storage
    agent >> cache
    
    resource_monitor >> server
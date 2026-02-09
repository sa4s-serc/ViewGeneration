from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus

with Diagram("Instana Hands-on Labs Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Diagram("Kubernetes Cluster", show=False, direction="TB"):
        ingress = Nginx("Ingress Controller")
        
        with Diagram("Monitoring Stack", show=False, direction="LR"):
            instana_backend = Server("Instana Backend")
            instana_agent = Docker("Instana Agent")
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")
            
        with Diagram("Application Stack", show=False, direction="LR"):
            robot_shop = Docker("Robot Shop App")
            database = Postgresql("Application DB")
    
    user >> ingress
    ingress >> robot_shop
    robot_shop >> database
    instana_agent >> instana_backend
    robot_shop >> instana_agent
    prometheus >> grafana
    instana_agent >> prometheus
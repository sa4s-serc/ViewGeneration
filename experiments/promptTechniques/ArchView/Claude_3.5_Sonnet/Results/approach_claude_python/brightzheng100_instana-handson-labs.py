from diagrams import Diagram
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.database import MongoDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Master
from diagrams.onprem.network import Istio
from diagrams.custom import Custom
from diagrams.onprem.client import Client

with Diagram("Instana Labs Architecture", show=False, direction="TB"):
    users = Client("Lab Users")
    
    # Kubernetes Components
    master = Master("K8s Master")
    instana_backend = Pod("Instana Backend")
    instana_agent = Pod("Instana Agent")
    robot_shop = Pod("Robot Shop App")
    
    # Monitoring Stack
    prometheus = Prometheus("Prometheus")
    grafana = Grafana("Grafana")
    
    # Infrastructure Components  
    docker = Docker("Container Runtime")
    ingress = Nginx("Ingress")
    db = MongoDB("Database")
    queue = Kafka("Message Queue")
    mesh = Istio("Service Mesh")

    # Core Application Flow
    users >> ingress >> robot_shop
    robot_shop >> db
    robot_shop >> queue
    
    # Monitoring Flow
    instana_agent >> instana_backend
    master >> [instana_agent, robot_shop]
    
    # Infrastructure Dependencies
    docker >> [instana_agent, robot_shop]
    mesh >> [instana_agent, robot_shop]
    
    # Metrics Flow
    instana_agent >> prometheus >> grafana
from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git

with Diagram("System Architecture", show=False, direction="LR"):
    user = User("End User")
    
    with Cluster("Web Layer"):
        lb = Nginx("Load Balancer")
        web_server1 = Server("Web Server 1")
        web_server2 = Server("Web Server 2")
    
    with Cluster("Application Layer"):
        app_server1 = Server("App Server 1")
        app_server2 = Server("App Server 2")
        message_queue = RabbitMQ("Message Queue")
    
    with Cluster("Data Layer"):
        primary_db = PostgreSQL("Primary DB")
        replica_db = PostgreSQL("Replica DB")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        loki = Loki("Loki")
    
    with Cluster("CI/CD"):
        git_repo = Git("Git Repository")
        jenkins = Jenkins("Jenkins")
        docker = Docker("Docker Registry")
    
    user >> lb
    lb >> web_server1
    lb >> web_server2
    web_server1 >> app_server1
    web_server2 >> app_server2
    app_server1 >> message_queue
    app_server2 >> message_queue
    app_server1 >> primary_db
    app_server2 >> primary_db
    primary_db >> replica_db
    
    app_server1 >> prometheus
    app_server2 >> prometheus
    prometheus >> grafana
    app_server1 >> loki
    app_server2 >> loki
    
    git_repo >> jenkins
    jenkins >> docker
    docker >> app_server1
    docker >> app_server2
import diagrams
from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Postgresql
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.logging import Fluentbit

with Diagram("System Architecture", show=False):
    user = User("User")
    
    with Cluster("Web Tier"):
        lb = Nginx("Load Balancer")
        web_server1 = Server("Web Server 1")
        web_server2 = Server("Web Server 2")
    
    with Cluster("Application Tier"):
        app_server1 = Server("App Server 1")
        app_server2 = Server("App Server 2")
    
    with Cluster("Data Tier"):
        db_primary = Postgresql("Primary DB")
        db_replica = Postgresql("Replica DB")
    
    with Cluster("Message Queue"):
        kafka = Kafka("Kafka")
    
    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
    
    with Cluster("CI/CD"):
        jenkins = Jenkins("Jenkins")
        docker = Docker("Docker")
        terraform = Terraform("Terraform")
    
    with Cluster("Data Processing"):
        airflow = Airflow("Airflow")
        fluentd = Fluentbit("Fluentd")
    
    user >> lb
    lb >> web_server1
    lb >> web_server2
    web_server1 >> app_server1
    web_server2 >> app_server2
    app_server1 >> db_primary
    app_server2 >> db_primary
    app_server1 >> db_replica
    app_server2 >> db_replica
    app_server1 >> kafka
    app_server2 >> kafka
    kafka >> airflow
    fluentd >> kafka
    prometheus >> grafana
    jenkins >> docker
    jenkins >> terraform
    docker >> app_server1
    docker >> app_server2
    terraform >> web_server1
    terraform >> web_server2
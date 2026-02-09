from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker

with Diagram("System Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Web Tier"):
        lb = Nginx("Load Balancer")
        web_server1 = Server("Web Server 1")
        web_server2 = Server("Web Server 2")
        web_server3 = Server("Web Server 3")
    
    with Cluster("Application Tier"):
        app_server1 = Server("App Server 1")
        app_server2 = Server("App Server 2")
    
    with Cluster("Data Tier"):
        db_primary = Postgresql("Primary DB")
        db_replica = Postgresql("Replica DB")
    
    with Cluster("Messaging"):
        kafka = Kafka("Message Broker")
    
    with Cluster("Monitoring"):
        grafana = Grafana("Dashboard")
        fluentbit = Fluentbit("Log Collector")
    
    with Cluster("CI/CD"):
        jenkins = Jenkins("Build Server")
        docker = Docker("Container Registry")
    
    user >> lb
    lb >> web_server1
    lb >> web_server2
    lb >> web_server3
    web_server1 >> app_server1
    web_server2 >> app_server1
    web_server3 >> app_server1
    web_server1 >> app_server2
    web_server2 >> app_server2
    web_server3 >> app_server2
    app_server1 >> db_primary
    app_server2 >> db_primary
    app_server1 >> db_replica
    app_server2 >> db_replica
    app_server1 >> kafka
    app_server2 >> kafka
    web_server1 >> fluentbit
    web_server2 >> fluentbit
    web_server3 >> fluentbit
    fluentbit >> grafana
    jenkins >> docker
    docker >> web_server1
    docker >> web_server2
    docker >> web_server3
    docker >> app_server1
    docker >> app_server2
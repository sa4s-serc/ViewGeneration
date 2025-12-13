from diagrams import Diagram, Cluster
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Mongodb
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Ansible
from diagrams.onprem.compute import Server

with Diagram("Microservices Architecture", show=False, direction="LR"):
    with Cluster("CI/CD Pipeline"):
        git = Git("Git Repository")
        jenkins = Jenkins("Jenkins")
        ansible = Ansible("Ansible")
        ci_cd = [git >> jenkins >> ansible]

    with Cluster("Application Layer"):
        with Cluster("Web Tier"):
            nginx = Nginx("Nginx")
            
        with Cluster("Microservices"):
            with Cluster("Service A"):
                service_a = Docker("Service A")
                db_a = Mongodb("MongoDB A")
                service_a >> db_a
                
            with Cluster("Service B"):
                service_b = Docker("Service B")
                db_b = Mongodb("MongoDB B")
                service_b >> db_b
                
            with Cluster("Service C"):
                service_c = Docker("Service C")
                db_c = Mongodb("MongoDB C")
                service_c >> db_c

        with Cluster("Message Queue"):
            kafka = Kafka("Kafka")
            
        with Cluster("Cache Layer"):
            redis = Redis("Redis")

    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        loki = Loki("Loki")
        prometheus >> grafana
        loki >> grafana

    with Cluster("Infrastructure"):
        server = Server("Bare Metal")

    # Connections
    nginx >> [service_a, service_b, service_c]
    [service_a, service_b, service_c] >> kafka
    [service_a, service_b, service_c] >> redis
    ansible >> server
    [service_a, service_b, service_c, nginx, kafka, redis] >> prometheus
    [service_a, service_b, service_c, nginx, kafka, redis] >> loki
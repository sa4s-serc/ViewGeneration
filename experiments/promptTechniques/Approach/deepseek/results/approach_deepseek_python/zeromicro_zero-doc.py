from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow

with Diagram("Microservices Architecture", show=False, direction="TB"):
    with Cluster("Load Balancer"):
        lb = Nginx("Nginx")

    with Cluster("API Gateway"):
        api_gateway = Server("API Gateway")

    with Cluster("Microservices"):
        with Cluster("Service A"):
            svc_a = Server("Service A")
            db_a = PostgreSQL("DB A")

        with Cluster("Service B"):
            svc_b = Server("Service B")
            db_b = PostgreSQL("DB B")

        with Cluster("Service C"):
            svc_c = Server("Service C")
            db_c = PostgreSQL("DB C")

    with Cluster("Message Queue"):
        mq = Kafka("Kafka")

    with Cluster("Monitoring"):
        prom = Prometheus("Prometheus")
        grafana = Grafana("Grafana")

    with Cluster("Cache"):
        cache = Redis("Redis")

    with Cluster("CI/CD"):
        ci_cd = Jenkins("Jenkins")
        docker = Docker("Docker")
        airflow = Airflow("Airflow")

    lb >> api_gateway
    api_gateway >> [svc_a, svc_b, svc_c]
    svc_a >> db_a
    svc_b >> db_b
    svc_c >> db_c
    [svc_a, svc_b, svc_c] >> mq
    [svc_a, svc_b, svc_c] >> cache
    [svc_a, svc_b, svc_c] >> prom
    prom >> grafana
    ci_cd >> docker
    ci_cd >> airflow
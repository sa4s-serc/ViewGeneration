from diagrams import Diagram, Cluster
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki

with Diagram("System Architecture", show=False):
    with Cluster("Load Balancer"):
        lb = Nginx("Nginx")

    with Cluster("Application Layer"):
        app1 = Server("App Server 1")
        app2 = Server("App Server 2")
        app3 = Server("App Server 3")

    with Cluster("Database Layer"):
        db_primary = PostgreSQL("Primary DB")
        db_replica = PostgreSQL("Replica DB")

    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        loki = Loki("Loki")

    with Cluster("CI/CD"):
        jenkins = Jenkins("Jenkins")
        docker = Docker("Docker Registry")

    lb >> [app1, app2, app3]
    [app1, app2, app3] >> db_primary
    db_primary >> db_replica
    [app1, app2, app3] >> prometheus
    prometheus >> grafana
    [app1, app2, app3] >> loki
    jenkins >> docker
    docker >> [app1, app2, app3]
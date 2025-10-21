from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Etcd
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Prometheus
from diagrams.saas.monitoring import Grafana
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Go
from diagrams.generic.blank import Blank

with Diagram("Go-Zero Framework Overview", show=False):
    user = User("Client")

    with Cluster("API Gateway"):
        api_gateway = Go("API Gateway")
        user >> Edge(label="HTTP Request") >> api_gateway

    with Cluster("Microservices"):
        with Cluster("Service 1"):
            svc1_api = Go("API Service")
            svc1_logic = Go("Logic")
            svc1_model = PostgreSQL("Database")
            svc1_api >> Edge(label="calls") >> svc1_logic >> Edge(label="queries") >> svc1_model

        with Cluster("Service 2"):
            svc2_api = Go("RPC Service")
            svc2_logic = Go("Logic")
            svc2_model = PostgreSQL("Database")
            svc2_api >> Edge(label="calls") >> svc2_logic >> Edge(label="queries") >> svc2_model

    api_gateway >> Edge(label="REST/RPC") >> [svc1_api, svc2_api]

    with Cluster("Infrastructure"):
        etcd = Etcd("Service Discovery")
        kafka = Kafka("Message Queue")
        prom = Prometheus("Metrics")
        grafana = Grafana("Visualization")
        docker = Docker("Containerization")

        svc1_api >> Edge(label="discovers") >> etcd
        svc2_api >> Edge(label="discovers") >> etcd

        [svc1_api, svc2_api] >> Edge(label="produces") >> kafka
        [svc1_api, svc2_api] >> Edge(label="monitored by") >> prom
        prom >> grafana

        [svc1_api, svc2_api] >> Edge(label="deployed on") >> docker

    user << Edge(label="HTTP Response") << api_gateway
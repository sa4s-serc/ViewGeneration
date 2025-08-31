from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.client import Client

with Diagram("Architectural View", show=True):
    client = Client("User")

    with Cluster("Service Cluster"):
        load_balancer = ELB("Load Balancer")
        service1 = EC2("Service 1")
        service2 = EC2("Service 2")
        db = RDS("Database")

        load_balancer >> Edge(label="HTTP Request") >> service1
        load_balancer >> Edge(label="HTTP Request") >> service2
        service1 >> Edge(label="SQL Query") >> db
        service2 >> Edge(label="SQL Query") >> db

    client >> Edge(label="HTTP Request") >> load_balancer
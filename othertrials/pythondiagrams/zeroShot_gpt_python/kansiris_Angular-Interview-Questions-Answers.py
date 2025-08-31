from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS
from diagrams.onprem.client import User

with Diagram("Scalable Web Service Architecture", show=True, direction="LR"):
    user = User("Client")

    with Cluster("Load Balancer"):
        lb = ELB("Elastic Load Balancer")

    with Cluster("Web Server Tier"):
        web_server_1 = EC2("Web Server 1")
        web_server_2 = EC2("Web Server 2")
        web_servers = [web_server_1, web_server_2]

    with Cluster("Database Tier"):
        primary_db = RDS("Primary DB")
        replica_db = RDS("Replica DB")

    queue = SQS("Message Queue")

    user >> lb >> web_servers
    web_servers >> Edge(label="Read/Write") >> primary_db
    primary_db >> Edge(label="Replicate") >> replica_db
    web_servers >> Edge(label="Queue Messages") >> queue
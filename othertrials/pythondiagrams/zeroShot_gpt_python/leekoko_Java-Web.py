from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS

with Diagram("Microservices Architecture", show=True, direction="TB"):
    with Cluster("Services Cluster"):
        service1 = EC2("Service 1")
        service2 = EC2("Service 2")
        service3 = EC2("Service 3")

    load_balancer = ELB("Load Balancer")
    queue = SQS("Message Queue")
    database = RDS("Database")

    load_balancer >> Edge(label="HTTP Request") >> service1
    load_balancer >> Edge(label="HTTP Request") >> service2
    load_balancer >> Edge(label="HTTP Request") >> service3

    service1 >> Edge(label="Message") >> queue
    service2 >> Edge(label="Message") >> queue
    service3 >> Edge(label="Message") >> queue

    queue >> Edge(label="Read") >> database
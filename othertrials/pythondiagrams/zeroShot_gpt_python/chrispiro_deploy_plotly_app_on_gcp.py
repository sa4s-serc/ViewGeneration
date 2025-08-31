from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS

with Diagram("System Architecture", show=True, direction="TB"):
    with Cluster("Load Balancing"):
        lb = ELB("Load Balancer")

    with Cluster("Application Layer"):
        with Cluster("Microservices"):
            svc1 = EC2("Service 1")
            svc2 = EC2("Service 2")
            svc3 = EC2("Service 3")

    with Cluster("Database Layer"):
        db_primary = RDS("Primary DB")
        db_replica = RDS("Replica DB")

    queue = SQS("Message Queue")

    lb >> svc1
    lb >> svc2
    lb >> svc3

    svc1 >> Edge(color="black", style="dashed") >> queue
    svc2 >> Edge(color="black", style="dashed") >> queue
    svc3 >> Edge(color="black", style="dashed") >> queue

    queue >> db_primary
    db_primary - db_replica
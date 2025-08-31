from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS
from diagrams.custom import Custom

with Diagram("Microservices Architecture", show=True, direction="TB"):
    with Cluster("User Interface"):
        user = Custom("User", "./icons/user.png")

    with Cluster("Service Layer"):
        svc1 = EC2("Service 1")
        svc2 = EC2("Service 2")
        svc3 = EC2("Service 3")

    with Cluster("Data Layer"):
        rds = RDS("Database")

    queue = SQS("Message Queue")

    user >> Edge(label="HTTP") >> ELB("Load Balancer") >> svc1
    svc1 >> Edge(label="gRPC", color="red") >> svc2
    svc2 >> Edge(label="REST", color="blue") >> svc3
    svc3 >> Edge(label="JDBC", color="green") >> rds
    svc1 >> Edge(label="Event", style="dotted") >> queue
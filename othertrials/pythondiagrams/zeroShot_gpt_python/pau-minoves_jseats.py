from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS

with Diagram("Microservices Architecture", show=False):
    with Cluster("Service Cluster"):
        svc_a = EC2("Service A")
        svc_b = EC2("Service B")
        svc_c = EC2("Service C")

    with Cluster("Database Cluster"):
        db_primary = RDS("RDS Primary")
        db_replica = RDS("RDS Replica")
        db_primary - Edge(label="replication") >> db_replica

    svc_a >> Edge(label="API Call") >> svc_b
    svc_b >> Edge(label="API Call") >> svc_c

    load_balancer = ELB("Load Balancer")
    load_balancer >> svc_a
    load_balancer >> svc_b
    load_balancer >> svc_c

    queue = SQS("Message Queue")
    svc_a >> Edge(label="sends message") >> queue
    queue >> Edge(label="receives message") >> svc_c
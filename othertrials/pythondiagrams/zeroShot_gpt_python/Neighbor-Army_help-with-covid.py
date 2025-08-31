from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS

with Diagram("Microservices Architecture", show=True, direction="TB"):
    with Cluster("Service Cluster"):
        svc1 = EC2("Service 1")
        svc2 = EC2("Service 2")
        svc3 = EC2("Service 3")
        
        svc1 - Edge(color="blue", label="REST API") - svc2
        svc2 - Edge(color="green", style="dashed", label="Msg Queue") >> SQS("Message Queue")
        svc3 - Edge(color="red", style="dotted", label="Function Call") - svc1
    
    db = RDS("Database")
    lb = ELB("Load Balancer")
    
    lb >> svc1
    lb >> svc2
    lb >> svc3
    svc1 >> db
    svc2 >> db
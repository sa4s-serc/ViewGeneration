from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS

with Diagram("Sample Architecture", show=False, direction="TB"):
    with Cluster("Layer 1: Load Balancing"):
        lb = ELB("load balancer")

    with Cluster("Layer 2: Application Layer"):
        with Cluster("Microservices"):
            svc1 = EC2("service 1")
            svc2 = EC2("service 2")
            svc3 = EC2("service 3")
        
        with Cluster("API Gateway"):
            api = EC2("API Gateway")

    with Cluster("Layer 3: Data Layer"):
        db = RDS("database")

    queue = SQS("message queue")

    lb >> api
    api >> Edge(color="darkorange") >> [svc1, svc2, svc3]
    svc1 >> Edge(color="blue", style="dashed") >> queue
    svc2 >> Edge(color="blue", style="dashed") >> queue
    svc3 >> Edge(color="blue", style="dashed") >> queue
    queue >> Edge(color="green", style="bold") >> db
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom

with Diagram("System Architecture", show=True, direction="TB"):
    with Cluster("VPC"):
        lb = ELB("Load Balancer")
        
        with Cluster("Services"):
            svc1 = EC2("Service 1")
            svc2 = EC2("Service 2")
            svc3 = EC2("Service 3")

    db = RDS("Database")

    lb >> Edge(color="blue", style="dashed") >> svc1
    lb >> Edge(color="blue", style="dashed") >> svc2
    lb >> Edge(color="blue", style="dashed") >> svc3
    svc1 >> Edge(color="red", style="solid") >> db
    svc2 >> Edge(color="red", style="solid") >> db
    svc3 >> Edge(color="red", style="solid") >> db

    legend_icon = Custom("Legend", "./legend.png")
    legend_icon - Edge(label="Legend", color="black") - lb
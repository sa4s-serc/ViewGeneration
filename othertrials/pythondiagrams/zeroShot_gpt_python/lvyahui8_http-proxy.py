from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS

with Diagram("Architectural View", show=True, direction="TB"):
    with Cluster("User Interaction Layer"):
        user = Custom("User", "./user_icon.png")

    with Cluster("Application Layer"):
        with Cluster("Microservices"):
            service1 = EC2("Service 1")
            service2 = EC2("Service 2")
            service3 = EC2("Service 3")

    with Cluster("Data Layer"):
        database = RDS("Database")

    load_balancer = ELB("Load Balancer")

    user >> load_balancer
    load_balancer >> Edge(label="REST API", color="blue", style="dashed") >> service1
    load_balancer >> Edge(label="REST API", color="blue", style="dashed") >> service2
    load_balancer >> Edge(label="REST API", color="blue", style="dashed") >> service3

    service1 >> Edge(label="SQL Query", color="red") >> database
    service2 >> Edge(label="SQL Query", color="red") >> database
    service3 >> Edge(label="SQL Query", color="red") >> database
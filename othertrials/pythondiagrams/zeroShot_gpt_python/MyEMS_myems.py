from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet

with Diagram("Architectural View", show=False, direction="TB"):
    user = User("User")

    with Cluster("System"):
        with Cluster("Frontend"):
            load_balancer = ELB("Load Balancer")
            web_service = EC2("Web Service")

        with Cluster("Backend"):
            app_service = EC2("App Service")
            database = RDS("Database")

    user >> Edge(label="request", color="blue") >> load_balancer
    load_balancer >> Edge(label="forward", color="blue") >> web_service
    web_service >> Edge(label="call", color="green") >> app_service
    app_service >> Edge(label="query", color="red") >> database
    database >> Edge(label="response", color="red") >> app_service
    app_service >> Edge(label="response", color="green") >> web_service
    web_service >> Edge(label="response", color="blue") >> load_balancer
    load_balancer >> Edge(label="response", color="blue") >> user
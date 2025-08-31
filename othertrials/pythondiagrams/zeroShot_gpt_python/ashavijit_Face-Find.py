from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.generic.os import Windows
from diagrams.programming.language import Python

with Diagram("Architectural View", show=True, direction="LR", outformat="png"):
    with Cluster("Client Layer"):
        client = Windows("Client")

    with Cluster("Application Layer"):
        app_server = EC2("Application Server")
        api_server = Python("API Server")

    with Cluster("Database Layer"):
        database = RDS("Database")

    client >> Edge(label="HTTP Request", color="blue") >> app_server
    app_server >> Edge(label="API Call", color="green") >> api_server
    api_server >> Edge(label="SQL Query", color="red") >> database
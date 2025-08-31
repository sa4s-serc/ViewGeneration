from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.generic.os import Windows, Linux

with Diagram("Architectural View Diagram", show=True, direction="TB"):
    with Cluster("Client Layer"):
        client = Windows("Client")

    with Cluster("Load Balancer"):
        lb = ELB("Load Balancer")

    with Cluster("Web Tier"):
        with Cluster("Web Server Group"):
            web_server_1 = EC2("Web Server 1")
            web_server_2 = EC2("Web Server 2")

    with Cluster("Database Tier"):
        db_master = RDS("Master DB")
        db_slave = RDS("Slave DB")
    
    client >> Edge(label="HTTP Request") >> lb
    lb >> Edge(label="Distributes Traffic", forward=True) >> [web_server_1, web_server_2]
    web_server_1 >> Edge(label="SQL Query", style="dotted") >> db_master
    web_server_2 >> Edge(label="SQL Query", style="dotted") >> db_slave
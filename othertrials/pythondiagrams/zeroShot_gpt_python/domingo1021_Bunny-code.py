from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.client import User

with Diagram("Architecture Overview", show=False, direction="TB"):
    user = User("Client")

    with Cluster("Web Tier"):
        lb = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"),
                       EC2("Web Server 2"),
                       EC2("Web Server 3")]

    with Cluster("Data Tier"):
        db_primary = RDS("Primary DB")
        db_replica = RDS("Replica DB")

    user >> lb >> web_servers
    web_servers >> Edge(color="brown", style="dashed") >> db_primary
    db_primary - Edge(color="blue", style="solid") - db_replica
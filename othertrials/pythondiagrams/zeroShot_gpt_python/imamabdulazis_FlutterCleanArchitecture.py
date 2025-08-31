from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS
from diagrams.aws.general import Users

with Diagram("Architectural View", show=False, direction="TB"):
    user = Users("User")

    with Cluster("Web Tier"):
        load_balancer = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"),
                       EC2("Web Server 2")]

    with Cluster("Application Tier"):
        app_servers = [EC2("App Server 1"),
                       EC2("App Server 2")]

    with Cluster("Data Tier"):
        database = RDS("Database")

    queue = SQS("Message Queue")

    user >> Edge(label="HTTP", color="blue") >> load_balancer
    load_balancer >> Edge(label="HTTP", color="blue") >> web_servers
    for web_server in web_servers:
        web_server >> Edge(label="HTTPS", color="green") >> app_servers
    for app_server in app_servers:
        app_server >> Edge(label="JDBC", color="brown") >> database
        app_server >> Edge(label="SQS", color="orange") >> queue
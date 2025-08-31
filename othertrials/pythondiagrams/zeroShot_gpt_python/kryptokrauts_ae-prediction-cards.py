from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS
from diagrams.aws.general import User

with Diagram("Architecture View Diagram", show=True, direction="TB"):
    user = User("User")

    with Cluster("Web Tier"):
        load_balancer = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"),
                       EC2("Web Server 2")]

    with Cluster("Application Tier"):
        app_servers = [EC2("App Server 1"),
                       EC2("App Server 2")]

    with Cluster("Database Tier"):
        database = RDS("Database")

    queue = SQS("Message Queue")

    user >> load_balancer
    load_balancer >> web_servers
    web_servers >> app_servers
    app_servers >> queue
    queue >> app_servers
    app_servers >> database
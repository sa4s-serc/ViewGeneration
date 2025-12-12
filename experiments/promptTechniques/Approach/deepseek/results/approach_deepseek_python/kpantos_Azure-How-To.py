from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS

with Diagram("Web Service Architecture", show=False):
    lb = ELB("Load Balancer")
    web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    db = RDS("Database")

    lb >> web_servers >> db
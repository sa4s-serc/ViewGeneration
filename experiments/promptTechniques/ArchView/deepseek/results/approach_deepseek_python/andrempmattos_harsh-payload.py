from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Architectural View", show=False):
    load_balancer = ELB("Load Balancer")
    web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    database = RDS("Database")
    storage = S3("Storage")

    load_balancer >> web_servers >> database
    web_servers >> storage
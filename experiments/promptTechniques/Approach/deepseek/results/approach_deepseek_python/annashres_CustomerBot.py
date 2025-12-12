from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Architectural View", show=False):
    lb = ELB("Load Balancer")
    web_servers = [EC2("Web Server 1"),
                   EC2("Web Server 2"),
                   EC2("Web Server 3")]
    db = RDS("Database")
    storage = S3("Storage")

    lb >> web_servers >> db
    web_servers >> storage
from diagrams import Diagram
from diagrams.aws.general import User
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Architectural View", show=False):
    user = User("User")
    lb = ELB("Load Balancer")
    web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    database = RDS("Database")
    storage = S3("Storage")

    user >> lb >> web_servers
    web_servers >> database
    web_servers >> storage
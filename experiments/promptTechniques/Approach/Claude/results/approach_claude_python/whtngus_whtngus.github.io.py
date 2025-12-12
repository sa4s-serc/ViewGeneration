from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Basic Web Architecture", show=False, direction="LR"):
    lb = ELB("Load Balancer")
    web = EC2("Web Server")
    db = RDS("Database")
    storage = S3("Static Storage")

    lb >> web
    web >> db
    web >> storage
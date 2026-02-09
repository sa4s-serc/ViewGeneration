from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Architecture Overview", show=False):
    lb = ELB("Load Balancer")
    web = EC2("Web Server")
    db = RDS("Database")
    storage = S3("Storage")
    
    lb >> web >> db
    web >> storage
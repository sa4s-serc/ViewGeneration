from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Web Service Architecture", show=False):
    lb = ELB("Load Balancer")
    
    with Cluster("Web Tier"):
        web = [
            EC2("Web Server 1"),
            EC2("Web Server 2")
        ]
    
    with Cluster("Database Tier"):
        db = RDS("Users Database")
        storage = S3("File Storage")
    
    lb >> web
    web >> db
    web >> storage
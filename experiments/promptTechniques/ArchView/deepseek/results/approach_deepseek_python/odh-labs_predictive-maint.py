from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Architecture View", show=False):
    lb = ELB("Load Balancer")
    
    with Cluster("Web Tier"):
        web_servers = [EC2("Web Server 1"),
                      EC2("Web Server 2"),
                      EC2("Web Server 3")]
    
    with Cluster("Database Tier"):
        db_master = RDS("Master DB")
        db_master - [RDS("Slave DB 1"),
                    RDS("Slave DB 2")]
    
    with Cluster("Storage Tier"):
        storage = S3("Object Storage")
    
    lb >> web_servers >> db_master
    web_servers >> storage
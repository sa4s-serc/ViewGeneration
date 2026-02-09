from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("Web Application Architecture", show=False):
    dns = Route53("DNS")
    lb = ELB("Load Balancer")
    
    with Cluster("Web Tier"):
        web_servers = [EC2("Web Server 1"),
                      EC2("Web Server 2"),
                      EC2("Web Server 3")]
    
    with Cluster("Database Tier"):
        db_primary = RDS("Primary DB")
        db_primary - [RDS("Read Replica 1"),
                     RDS("Read Replica 2")]
    
    storage = S3("Object Storage")
    
    User("User") >> dns >> lb >> web_servers
    web_servers >> db_primary
    web_servers >> storage
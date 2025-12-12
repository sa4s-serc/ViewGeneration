from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Web Service Architecture", show=False):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
    EC2("Web Server") >> S3("Storage")
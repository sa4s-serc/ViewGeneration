from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("VR Scene Exploration Application Architecture", show=False):
    user = User("User")
    load_balancer = ELB("Load Balancer")
    web_server = EC2("Web Server")
    database = RDS("Database")
    storage = S3("Storage")

    user >> load_balancer >> web_server
    web_server >> database
    web_server >> storage
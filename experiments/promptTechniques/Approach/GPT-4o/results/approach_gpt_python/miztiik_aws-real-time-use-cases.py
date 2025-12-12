from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("AWS Real-Time Use Cases", show=False, direction="TB"):

    with Cluster("Client-Server Architecture"):
        client = EC2("Client")
        server = EC2("Server")

    with Cluster("AWS Services"):
        load_balancer = ELB("Load Balancer")
        storage = S3("Storage")
        database = RDS("Database")
        queue = SQS("Message Queue")

    client >> load_balancer
    load_balancer >> server
    server >> database
    server >> queue
    server >> storage
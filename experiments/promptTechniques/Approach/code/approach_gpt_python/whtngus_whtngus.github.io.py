from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS
from diagrams.generic.storage import Storage

with Diagram("Architectural View Diagram", show=False):
    with Cluster("Load Balancing Layer"):
        lb = ELB("Load Balancer")

    with Cluster("Application Layer"):
        app1 = EC2("App Server 1")
        app2 = EC2("App Server 2")

    with Cluster("Database Layer"):
        master_db = RDS("Master DB")
        slave_db = RDS("Slave DB")

    with Cluster("Queue System"):
        queue = SQS("Message Queue")

    with Cluster("Storage System"):
        storage = Storage("Blob Storage")

    lb >> app1
    lb >> app2
    app1 >> master_db
    app2 >> master_db
    master_db - slave_db
    app1 >> queue
    app2 >> queue
    app1 >> storage
    app2 >> storage
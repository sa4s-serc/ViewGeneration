from diagrams import Diagram, Cluster, Node
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server

with Diagram("Django-based IDS Architecture", show=False):
    user = User("User")

    with Cluster("Web Interface"):
        load_balancer = ELB("Load Balancer")
        web_servers = [Server("Django App 1"),
                       Server("Django App 2")]

    db = RDS("SQLite DB")

    with Cluster("Intrusion Detection System"):
        ml_model = Node("Random Forest Classifier")
        file_proc = Node("File Processor")

    user >> load_balancer >> web_servers
    web_servers >> db
    web_servers >> ml_model
    web_servers >> file_proc
    file_proc >> ml_model
    ml_model >> db
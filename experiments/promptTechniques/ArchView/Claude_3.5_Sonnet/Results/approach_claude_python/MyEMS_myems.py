from diagrams import Diagram, Cluster
from diagrams.aws.database import RDS
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.onprem.client import Users
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.security import IAM
from diagrams.aws.network import APIGateway

with Diagram("MyEMS Architecture", show=False):
    users = Users("End Users")
    
    with Cluster("MyEMS System"):
        api = APIGateway("RESTful API\n(Falcon)")
        
        with Cluster("Authentication"):
            iam = IAM("User Auth")
        
        with Cluster("Processing Layer"):
            app = EC2("Application\nServers")
            queue = SQS("Message\nQueue")
            
        with Cluster("Data Layer"):
            db = RDS("MySQL\nDatabases")
            storage = S3("File\nStorage")
            
        with Cluster("Load Balancing"):
            lb = ELB("Load\nBalancer")
    
    # Flow definition
    users >> lb >> api >> iam
    api >> app 
    app >> queue
    app >> db
    app >> storage
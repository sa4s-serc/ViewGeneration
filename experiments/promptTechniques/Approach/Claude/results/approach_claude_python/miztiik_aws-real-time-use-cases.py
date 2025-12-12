from diagrams import Diagram, Cluster
from diagrams.aws.general import Client, Users
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Database
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM
from diagrams.aws.network import VPC, InternetGateway
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS, SNS

with Diagram("AWS Real-Time Use Cases Architecture", show=False):
    users = Users("End Users")
    
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            gateway = InternetGateway("Internet Gateway")
            
            with Cluster("Application Layer"):
                ec2 = EC2("Use Case Server")
                
            with Cluster("Data Layer"):
                db = RDS("Relational DB")
                dynamo = Database("NoSQL DB")
                storage = S3("Documentation Storage")
            
            with Cluster("Integration Layer"):
                queue = SQS("Message Queue")
                notification = SNS("Notifications")
            
            with Cluster("Management & Security"):
                monitoring = Cloudwatch("Monitoring")
                security = IAM("Access Control")

    users >> gateway >> ec2
    ec2 >> db
    ec2 >> dynamo
    ec2 >> storage
    ec2 >> queue
    queue >> notification
    ec2 >> monitoring
    security - ec2
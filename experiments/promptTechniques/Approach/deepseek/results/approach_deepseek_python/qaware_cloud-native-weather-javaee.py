from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("Cloud Native Weather Application Architecture", show=False):
    user = User("End User")
    
    with Cluster("Load Balancer"):
        lb = ELB("Application Load Balancer")
    
    with Cluster("Application Tier"):
        with Cluster("Auto Scaling Group"):
            app_instances = [EC2("Payara Micro\nInstance") for _ in range(2)]
    
    with Cluster("Data Tier"):
        db = RDS("PostgreSQL\nDatabase")
        cache = SQS("Message Queue")
        storage = S3("Object Storage")
    
    with Cluster("External Services"):
        external_api = EC2("OpenWeatherMap API")
    
    user >> lb >> app_instances
    app_instances >> db
    app_instances >> cache
    app_instances >> storage
    app_instances >> external_api
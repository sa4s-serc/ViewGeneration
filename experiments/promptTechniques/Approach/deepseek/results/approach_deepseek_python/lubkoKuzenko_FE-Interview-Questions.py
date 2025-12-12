from diagrams import Diagram, Cluster
from diagrams.aws.general import Users, InternetAlt1
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch

with Diagram("Frontend Interview Questions Architecture", show=False, direction="LR"):
    users = Users("Users")
    internet = InternetAlt1("Internet")
    
    with Cluster("AWS Cloud"):
        cdn = CloudFront("CDN")
        
        with Cluster("Application Layer"):
            with Cluster("Auto Scaling Group"):
                app_instances = [EC2("App Server 1"),
                               EC2("App Server 2"),
                               EC2("App Server N")]
        
        with Cluster("Data Layer"):
            database = RDS("Question Database")
            storage = S3("File Storage")
        
        monitoring = Cloudwatch("Monitoring")
        security = IAM("Security & Access")
    
    users >> internet >> cdn
    cdn >> app_instances
    app_instances >> database
    app_instances >> storage
    security - app_instances
    security - database
    security - storage
    monitoring >> app_instances
    monitoring >> database
    monitoring >> storage
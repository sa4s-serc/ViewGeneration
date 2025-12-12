from diagrams import Diagram, Cluster
from diagrams.aws.general import User, InternetAlt1
from diagrams.aws.security import IdentityAndAccessManagementIam
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis
from diagrams.aws.ml import Comprehend

with Diagram("2WAY_Design Architecture", show=False, direction="LR"):
    internet = InternetAlt1("Internet")
    
    with Cluster("Trust Network"):
        user1 = User("Trusted Party 1")
        user2 = User("Trusted Party 2")
        user3 = User("Trusted Party 3")
    
    with Cluster("Core Platform"):
        api = APIGateway("API Gateway")
        auth = IdentityAndAccessManagementIam("Authentication")
        
        with Cluster("Data Processing"):
            lambda_func = Lambda("Processing Function")
            kinesis = Kinesis("Data Stream")
            comprehend = Comprehend("Analysis")
        
        with Cluster("Storage"):
            s3 = S3("Private Data")
            dynamodb = Dynamodb("Trust Metadata")
    
    user1 >> internet >> api
    user2 >> internet >> api
    user3 >> internet >> api
    
    api >> auth
    auth >> lambda_func
    lambda_func >> kinesis
    kinesis >> comprehend
    comprehend >> s3
    lambda_func >> dynamodb
    dynamodb >> lambda_func
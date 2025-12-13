from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda, ECS, Fargate
from diagrams.aws.network import APIGateway, CloudFront, Route53, ELB, VPC
from diagrams.aws.database import Dynamodb, RDS
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis, Athena
from diagrams.aws.integration import SQS, SNS, Eventbridge
from diagrams.aws.security import Cognito, IAM, WAF
from diagrams.aws.management import Cloudwatch, Cloudtrail, SystemsManager
from diagrams.aws.migration import DMS
from diagrams.aws.general import User

with Diagram("Piattaforma Notifiche Infrastructure", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        cf = CloudFront("CDN")
        api_gw = APIGateway("API Gateway")
        waf = WAF("WAF")
        cognito = Cognito("Cognito")
        
    with Cluster("Application Layer"):
        with Cluster("Microservices"):
            ecs = ECS("ECS Cluster")
            fargate = Fargate("Fargate Tasks")
            lambda_func = Lambda("Lambda Functions")
            
        with Cluster("Event Processing"):
            event_bridge = Eventbridge("EventBridge")
            sns = SNS("SNS")
            sqs = SQS("SQS")
            
    with Cluster("Data Layer"):
        with Cluster("Databases"):
            dynamodb = Dynamodb("DynamoDB")
            rds = RDS("RDS")
            
        with Cluster("Storage"):
            s3 = S3("S3")
            kinesis = Kinesis("Kinesis")
            
        with Cluster("Analytics"):
            athena = Athena("Athena")
            dms = DMS("DMS")
            
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        cloudtrail = Cloudtrail("CloudTrail")
        ssm = SystemsManager("Systems Manager")
        
    user >> cf >> waf >> api_gw
    api_gw >> cognito
    api_gw >> lambda_func
    api_gw >> ecs
    ecs >> fargate
    fargate >> sqs
    fargate >> sns
    lambda_func >> event_bridge
    event_bridge >> sns
    sns >> sqs
    sqs >> dynamodb
    sqs >> rds
    sqs >> s3
    s3 >> kinesis
    kinesis >> athena
    athena >> dms
    ecs >> cloudwatch
    lambda_func >> cloudwatch
    api_gw >> cloudwatch
    dynamodb >> cloudtrail
    rds >> cloudtrail
    s3 >> cloudtrail
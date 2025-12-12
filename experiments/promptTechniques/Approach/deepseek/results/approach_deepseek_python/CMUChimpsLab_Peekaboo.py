from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.iot import Sensor
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Mqtt
from diagrams.aws.ml import Sagemaker
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.analytics import Kinesis
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import CloudFront, Route53, VPC, PublicSubnet, PrivateSubnet, NATGateway, InternetGateway, ElasticLoadBalancing
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import EFS
from diagrams.generic.blank import Blank
from diagrams.programming.framework import FastAPI
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.custom import Custom

with Diagram("Peekaboo Node-RED Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Node-RED Flow Environment"):
        node_red = Custom("Node-RED", "./resources/node-red.png")
        
        with Cluster("Provider Nodes"):
            pull_provider = Blank("Pull Provider")
            push_provider = Blank("Push Provider")
            sensor_provider = Sensor("Sensor Data")
            mqtt_provider = Mqtt("MQTT")
        
        with Cluster("Inference Nodes"):
            classify = Blank("Classify")
            detect = Blank("Detect")
            extract = Blank("Extract")
        
        with Cluster("Filter Nodes"):
            select = Blank("Select")
            noisify = Blank("Noisify")
            spoof = Blank("Spoof")
        
        with Cluster("Network Nodes"):
            post = Blank("Post")
        
        with Cluster("Utility Nodes"):
            aggregate = Blank("Aggregate")
            inject = Blank("pkbInject")
            join = Blank("pkbJoin")
    
    with Cluster("External Services"):
        with Cluster("Inference Services"):
            ml_services = Sagemaker("ML Services")
            custom_services = FastAPI("Custom Services")
        
        with Cluster("Data Storage"):
            s3 = S3("S3 Storage")
            dynamodb = Dynamodb("DynamoDB")
            redis = Redis("Redis Cache")
        
        with Cluster("Message Queues"):
            sqs = SQS("SQS")
            kinesis = Kinesis("Kinesis Streams")
    
    with Cluster("Infrastructure"):
        with Cluster("VPC"):
            igw = InternetGateway("IGW")
            
            with Cluster("Public Subnet"):
                alb = ElasticLoadBalancing("ALB")
                nginx = Nginx("Nginx")
            
            with Cluster("Private Subnet"):
                with Cluster("Application Layer"):
                    ec2_app = EC2("App Servers")
                    lambda_func = Lambda("Lambda Functions")
                
                with Cluster("Data Layer"):
                    rds = RDS("RDS")
                    efs = EFS("EFS")
    
    with Cluster("Management & Monitoring"):
        iam = IAM("IAM")
        cloudwatch = Cloudwatch("CloudWatch")
        route53 = Route53("Route53")
        cloudfront = CloudFront("CloudFront")

    user >> node_red
    
    sensor_provider >> mqtt_provider
    pull_provider >> node_red
    push_provider >> node_red
    
    node_red >> classify >> ml_services
    node_red >> detect >> custom_services
    node_red >> extract >> ml_services
    
    node_red >> select >> s3
    node_red >> noisify >> dynamodb
    node_red >> spoof >> redis
    
    node_red >> post >> sqs
    node_red >> post >> kinesis
    
    node_red >> aggregate >> lambda_func
    node_red >> inject >> ec2_app
    node_red >> join >> rds
    
    ml_services >> s3
    custom_services >> dynamodb
    sqs >> lambda_func
    kinesis >> ec2_app
    
    alb >> nginx >> ec2_app
    ec2_app >> rds
    ec2_app >> efs
    
    igw >> alb
    route53 >> cloudfront >> alb
    
    iam >> ec2_app
    iam >> lambda_func
    cloudwatch >> ec2_app
    cloudwatch >> lambda_func
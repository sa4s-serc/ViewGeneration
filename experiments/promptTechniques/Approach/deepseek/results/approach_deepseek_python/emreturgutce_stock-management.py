from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.inmemory import Redis
from diagrams.aws.security import IAM
from diagrams.aws.ml import Sagemaker
from diagrams.aws.analytics import Glue
from diagrams.aws.integration import SQS
from diagrams.aws.mobile import APIGateway

with Diagram("Stock Management Application Backend", show=False, direction="TB"):
    with Cluster("Client Layer"):
        client = EC2("Web Client")
    
    with Cluster("API Gateway"):
        api_gateway = APIGateway("REST API Gateway")
    
    with Cluster("Application Layer"):
        with Cluster("Controllers"):
            personnel_ctrl = EC2("Personnel Controller")
            supplier_ctrl = EC2("Supplier Controller")
            car_ctrl = EC2("Car Controller")
            customer_ctrl = EC2("Customer Controller")
            sales_ctrl = EC2("Sales Controller")
        
        with Cluster("Middleware"):
            auth = EC2("Authentication")
            authorization = EC2("Authorization")
            validation = EC2("Validation")
            rate_limiting = EC2("Rate Limiting")
            error_handling = EC2("Error Handling")
    
    with Cluster("Data Layer"):
        with Cluster("Databases"):
            postgres = RDS("PostgreSQL")
            redis = Redis("Redis Cache")
        
        with Cluster("Storage"):
            s3 = S3("AWS S3")
    
    with Cluster("Security"):
        iam = IAM("IAM Roles")
    
    with Cluster("Background Processing"):
        sqs = SQS("Message Queue")
        glue = Glue("Data Processing")
    
    client >> api_gateway
    api_gateway >> personnel_ctrl
    api_gateway >> supplier_ctrl
    api_gateway >> car_ctrl
    api_gateway >> customer_ctrl
    api_gateway >> sales_ctrl
    personnel_ctrl >> auth
    supplier_ctrl >> validation
    car_ctrl >> validation
    customer_ctrl >> validation
    sales_ctrl >> validation
    auth >> authorization
    authorization >> rate_limiting
    rate_limiting >> error_handling
    error_handling >> postgres
    error_handling >> redis
    error_handling >> s3
    car_ctrl >> sqs
    sqs >> glue
    iam >> personnel_ctrl
    iam >> supplier_ctrl
    iam >> car_ctrl
    iam >> customer_ctrl
    iam >> sales_ctrl
    iam >> postgres
    iam >> s3
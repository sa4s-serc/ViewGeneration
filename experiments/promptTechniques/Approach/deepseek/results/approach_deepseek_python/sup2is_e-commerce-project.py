from diagrams import Diagram, Cluster
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.integration import SQS
from diagrams.aws.security import Cognito
from diagrams.aws.general import User
from diagrams.aws.network import Route53
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb

with Diagram("E-commerce Platform Architecture", show=False, direction="TB"):
    user = User("Customer")
    
    with Cluster("Frontend"):
        cdn = CloudFront("CDN")
        route53 = Route53("DNS")
    
    with Cluster("API Gateway"):
        api_gateway = APIGateway("API Gateway")
    
    with Cluster("Authentication"):
        cognito = Cognito("Cognito")
    
    with Cluster("Microservices"):
        with Cluster("Product Service"):
            product_service = ECS("Product Service")
            product_db = RDS("Product DB")
            product_cache = ElastiCache("Redis Cache")
        
        with Cluster("Order Service"):
            order_service = ECS("Order Service")
            order_db = RDS("Order DB")
        
        with Cluster("User Service"):
            user_service = ECS("User Service")
            user_db = Dynamodb("User DB")
        
        with Cluster("Payment Service"):
            payment_service = Lambda("Payment Service")
            payment_queue = SQS("Payment Queue")
    
    user >> route53 >> cdn >> api_gateway
    api_gateway >> cognito
    api_gateway >> product_service
    api_gateway >> order_service
    api_gateway >> user_service
    api_gateway >> payment_service
    
    product_service >> product_db
    product_service >> product_cache
    order_service >> order_db
    user_service >> user_db
    payment_service >> payment_queue
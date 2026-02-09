from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDSMysqlInstance, ElasticacheForRedis, DynamodbTable
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.integration import SQS, SNS
from diagrams.onprem.container import Docker

with Diagram("Bunny Code Platform Architecture", show=False):
    with Cluster("Frontend CDN"):
        cdn = CloudFront("CloudFront CDN")

    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        auth = Cognito("Authentication")

    with Cluster("Application Services"):
        with Cluster("Core Services"):
            api_server = EC2("API Server")
            compiler = Lambda("Code Compiler")
            sandbox = Docker("Code Sandbox")

        with Cluster("Real-time Services"):
            battle = EC2("Battle Service")
            workspace = EC2("Workspace Service")

    with Cluster("Message Services"):
        queue = SQS("Message Queue")
        notification = SNS("Notifications")

    with Cluster("Storage Layer"):
        with Cluster("Databases"):
            mysql = RDSMysqlInstance("MySQL")
            redis = ElasticacheForRedis("Redis Cache")
            timeseries = DynamodbTable("Time Series DB")
        
        object_store = S3("Code Storage")

    # Frontend to Backend
    cdn >> api
    api >> auth
    
    # API Flow
    api >> api_server
    api_server >> compiler
    compiler >> sandbox
    
    # Real-time Services
    api_server >> battle
    api_server >> workspace
    
    # Data Flow
    api_server >> mysql
    api_server >> redis
    battle >> timeseries
    workspace >> timeseries
    
    # Storage
    compiler >> object_store
    workspace >> object_store
    
    # Messaging
    api_server >> queue
    queue >> notification
    battle >> notification
    workspace >> notification
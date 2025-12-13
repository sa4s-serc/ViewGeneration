from diagrams import Diagram, Cluster
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import NodeJS

with Diagram("Stock Management Backend Architecture", show=False):
    with Cluster("Backend Services"):
        api = APIGateway("API Gateway")
        auth = Cognito("Authentication")
        
        with Cluster("Application Layer"):
            app = NodeJS("Node.js/Express")
            
        with Cluster("Data Storage"):
            db = RDS("PostgreSQL")
            cache = Redis("Redis Cache")
            storage = S3("S3 Storage")
            
        with Cluster("Containerization"):
            docker = Docker("Docker Container")
    
    # Connect components
    api >> auth
    auth >> app
    app >> docker
    docker >> db
    docker >> cache
    docker >> storage
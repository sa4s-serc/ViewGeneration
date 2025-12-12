from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway

with Diagram("Feedback Analysis System Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Diagram("Frontend Layer"):
        frontend = React("fas-web-app")
        hosting = S3("Firebase Hosting")
        frontend >> hosting
    
    with Diagram("Backend Layer"):
        api_gateway = APIGateway("API Gateway")
        auth = Cognito("User Authentication")
        
        with Diagram("Application Services"):
            search_service = Lambda("Search Service")
            analysis_service = Lambda("Analysis Service")
            dashboard_service = Lambda("Dashboard Service")
        
        with Diagram("Data Layer"):
            postgresql = PostgreSQL("User Data")
            dynamodb = Dynamodb("Analysis Results")
    
    user >> frontend
    frontend >> api_gateway
    api_gateway >> auth
    api_gateway >> search_service
    api_gateway >> analysis_service
    api_gateway >> dashboard_service
    
    search_service >> dynamodb
    analysis_service >> dynamodb
    dashboard_service >> dynamodb
    auth >> postgresql
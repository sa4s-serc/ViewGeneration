from diagrams import Diagram, Cluster
from diagrams.aws.mobile import Amplify
from diagrams.aws.compute import EC2
from diagrams.onprem.database import MongoDB
from diagrams.programming.language import NodeJS
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import React

with Diagram("Stotra Architecture", show=False):
    frontend = Amplify("Frontend Hosting")
    
    with Cluster("Frontend (React)"):
        react_app = React("React App")
        frontend >> react_app
    
    with Cluster("Backend (Node.js/Express)"):
        backend = NodeJS("Node.js Server")
        api_gateway = Nginx("API Gateway")
        backend >> api_gateway
        
        with Cluster("Services"):
            auth_service = NodeJS("Auth Service")
            stock_data_service = NodeJS("Stock Data Service")
            news_service = NodeJS("News Service")
            
        api_gateway >> auth_service
        api_gateway >> stock_data_service
        api_gateway >> news_service
    
    with Cluster("Database"):
        db = MongoDB("MongoDB Atlas")
    
    frontend >> api_gateway
    auth_service >> db
    stock_data_service >> db
    news_service >> db

    with Cluster("Hosting and Deployment"):
        docker = Docker("Containerization")
        ec2 = EC2("EC2 Instance")
        docker >> ec2
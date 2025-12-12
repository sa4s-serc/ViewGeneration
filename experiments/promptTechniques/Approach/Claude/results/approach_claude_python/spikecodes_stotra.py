from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, VPC
from diagrams.aws.storage import S3
from diagrams.programming.framework import React
from diagrams.programming.language import NodeJS
from diagrams.aws.security import Cognito 
from diagrams.aws.integration import SQS
from diagrams.aws.management import Cloudwatch

with Diagram("Stotra Trading Platform Architecture", show=False, direction="TB"):
    
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            # Frontend Layer
            frontend = React("React Frontend")
            
            # Load Balancer
            lb = ELB("Load Balancer")
            
            # Backend Services
            with Cluster("Backend Services"):
                api = NodeJS("Node.js API")
                auth = Cognito("Authentication")
                
            # Database Layer
            db = RDS("MongoDB")
            
            # Storage
            storage = S3("Static Assets")
            
            # Monitoring & Queue
            monitoring = Cloudwatch("Monitoring")
            queue = SQS("Message Queue")

    # Frontend Flow
    frontend >> lb >> api
    
    # Auth Flow
    api >> auth
    
    # Data Flow
    api >> db
    api >> storage
    
    # Background Processing
    api >> queue
    
    # Monitoring
    api >> monitoring
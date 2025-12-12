from diagrams import Diagram
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDSInstance
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.storage import S3
from diagrams.firebase.base import Firebase
from diagrams.programming.framework import React
from diagrams.aws.mobile import APIGateway

with Diagram("Indoor Map with Heatmap Architecture", show=False):
    # Frontend components
    client = React("iOS App")
    
    # API Gateway and CDN
    api = APIGateway("REST API")
    cdn = CloudFront("CDN")
    
    # Backend services
    backend = ECS("Node.js Backend")
    worker = Lambda("Event Processor")
    
    # Storage components
    db = RDSInstance("MongoDB")
    storage = S3("PDF Storage")
    realtime = Firebase("Realtime Events")
    
    # Client interactions
    client >> cdn >> storage
    client >> api >> backend
    
    # Backend interactions
    backend >> db
    backend >> storage
    backend - worker >> realtime
    
    # Event flow
    client >> realtime
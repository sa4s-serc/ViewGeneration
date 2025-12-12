from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.firebase.develop import Authentication
from diagrams.aws.mobile import APIGateway
from diagrams.gcp.ml import AIPlatform
from diagrams.programming.language import Swift, Kotlin
from diagrams.aws.database import Aurora
from diagrams.firebase.base import Firebase
from diagrams.gcp.compute import GKE
from diagrams.aws.storage import S3
from diagrams.gcp.network import LoadBalancing

with Diagram("CPR2U Architecture", show=False):
    with Cluster("Mobile Apps"):
        ios = Swift("iOS App")
        android = Kotlin("Android App")

    with Cluster("Backend Services"):
        api = APIGateway("REST API")
        auth = Authentication("Auth Service")
        ml = AIPlatform("ML Service")
        
        with Cluster("Database"):
            db = Aurora("Main DB")
        
        with Cluster("Storage"):
            storage = S3("File Storage")
        
        with Cluster("Real-time Services"):
            firebase = Firebase("Firebase")
            
        with Cluster("Deployment"):
            lb = LoadBalancing("Load Balancer")
            k8s = GKE("Kubernetes")

    # Mobile apps connections
    ios >> api
    android >> api
    
    # Auth flow
    ios >> auth
    android >> auth
    
    # ML connections
    ios >> ml
    android >> ml
    
    # Backend connections
    api >> db
    api >> storage
    api >> firebase
    
    # Deployment connections
    api >> lb >> k8s
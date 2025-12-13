from diagrams import Diagram
from diagrams.programming.framework import Django
from diagrams.onprem.database import PostgreSQL
from diagrams.aws.ml import Rekognition
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.generic.storage import Storage

with Diagram("Face-Find Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Diagram("Presentation Layer"):
        nginx = Nginx("Nginx")
        bootstrap = Storage("Bootstrap CSS")
    
    with Diagram("Backend Layer"):
        django = Django("Django App")
        
        with Diagram("Database Layer"):
            postgres = PostgreSQL("PostgreSQL")
            redis = Redis("Redis Cache")
        
        with Diagram("External Services"):
            azure_face = Rekognition("Azure Face API")
            email_service = Storage("Email Service")
    
    user >> nginx
    nginx >> django
    django >> postgres
    django >> redis
    django >> azure_face
    django >> email_service
    bootstrap - nginx
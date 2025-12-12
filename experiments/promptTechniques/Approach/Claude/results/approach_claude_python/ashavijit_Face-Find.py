from diagrams import Diagram, Cluster
from diagrams.programming.framework import Django
from diagrams.onprem.database import PostgreSQL
from diagrams.azure.storage import BlobStorage
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.integration import APIManagement
from diagrams.onprem.client import Users

with Diagram("Face-Find Architecture", show=False):
    with Cluster("Frontend"):
        users = Users("Web UI")
        
    with Cluster("Backend Layer"):
        django = Django("Django App")
        api = APIManagement("Azure Face API")
        auth = ActiveDirectory("Authentication")
        
    with Cluster("Data Layer"):
        db = PostgreSQL("PostgreSQL")
        storage = BlobStorage("Image Storage")
        
    users >> django
    django >> api
    django >> auth
    django >> db
    django >> storage
    
    api >> storage
    auth >> db
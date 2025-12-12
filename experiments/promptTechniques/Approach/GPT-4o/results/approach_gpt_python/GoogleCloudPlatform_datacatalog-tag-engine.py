from diagrams import Diagram, Cluster
from diagrams.gcp.compute import Run
from diagrams.gcp.database import Firestore
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.devtools import Tasks
from diagrams.gcp.security import Iam
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.generic.blank import Blank

with Diagram("Tag Engine v3 Architecture", show=False):
    client = Client("User")
    
    with Cluster("Google Cloud"):
        with Cluster("Cloud Run Services"):
            api_service = Run("API Service")
            ui_service = Run("UI Service")
        
        firestore = Firestore("Firestore")
        tasks = Tasks("Cloud Tasks")
        gcs = GCS("GCS")
        bq = BigQuery("BigQuery")
        iam = Iam("IAM")

        client >> ui_service
        ui_service >> firestore
        ui_service >> api_service
        api_service >> firestore
        api_service >> tasks
        api_service >> gcs
        api_service >> bq
        api_service >> iam
        
    bq >> Blank("Reports and Analysis")
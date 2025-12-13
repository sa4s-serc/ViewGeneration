from diagrams import Diagram
from diagrams.gcp.compute import Run
from diagrams.gcp.database import Firestore
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.security import IAP
from diagrams.gcp.devtools import Tasks
from diagrams.onprem.client import User
from diagrams.programming.framework import Flask

with Diagram("Tag Engine v3 Architecture", show=False, direction="TB"):
    users = User("Users")
    
    iap = IAP("Identity-Aware Proxy")
    lb = LoadBalancing("Load Balancer")
    
    ui_service = Run("UI Service")
    api_service = Run("API Service")
    
    flask_app = Flask("Flask Application")
    
    firestore = Firestore("Firestore\n(Configurations)")
    gcs = GCS("Cloud Storage\n(CSV Files)")
    bigquery = BigQuery("BigQuery\n(Tag History)")
    
    cloud_tasks = Tasks("Cloud Tasks")
    
    datacatalog = BigQuery("Data Catalog")
    dataplex = BigQuery("Dataplex")
    
    users >> iap >> lb
    
    lb >> ui_service
    lb >> api_service
    
    ui_service >> flask_app
    api_service >> flask_app
    
    flask_app >> firestore
    flask_app >> gcs
    flask_app >> bigquery
    flask_app >> cloud_tasks
    
    cloud_tasks >> datacatalog
    cloud_tasks >> dataplex
    
    flask_app >> datacatalog
    flask_app >> dataplex
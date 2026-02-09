from diagrams import Diagram, Cluster
from diagrams.gcp.compute import AppEngine
from diagrams.gcp.database import Bigtable
from diagrams.gcp.storage import GCS
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python
from diagrams.gcp.analytics import Bigquery
from diagrams.gcp.api import Endpoints

with Diagram("Data Visualization App on GCP", show=False, direction="TB"):
    user = Python("User")
    
    with Cluster("GCP Services"):
        app_engine = AppEngine("App Engine")
        
        with Cluster("Data Sources"):
            bigquery = Bigquery("BigQuery")
            cloud_storage = GCS("Cloud Storage")
        
        with Cluster("Application Components"):
            dash_app = Flask("Dash App")
            load_data = Python("load_data.py")
            create_charts = Python("create_charts.py")
    
    user >> app_engine
    app_engine >> dash_app
    dash_app >> load_data
    dash_app >> create_charts
    load_data >> bigquery
    load_data >> cloud_storage
    create_charts >> dash_app
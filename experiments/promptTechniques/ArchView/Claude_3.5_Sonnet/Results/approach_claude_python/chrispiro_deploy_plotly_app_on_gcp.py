from diagrams import Diagram, Cluster
from diagrams.gcp.compute import AppEngine
from diagrams.gcp.storage import Storage
from diagrams.programming.language import Python
from diagrams.gcp.analytics import Bigquery

with Diagram("Data Visualization App on GCP", show=False):
    with Cluster("Data Sources"):
        storage = Storage("Cloud Storage")
        bq = Bigquery("BigQuery")

    with Cluster("Application Components"):
        with Cluster("Core App"):
            python = Python("Python Backend")

    with Cluster("Deployment"):
        app_engine = AppEngine("App Engine")

    # Data flow
    storage >> python
    bq >> python
    python >> app_engine
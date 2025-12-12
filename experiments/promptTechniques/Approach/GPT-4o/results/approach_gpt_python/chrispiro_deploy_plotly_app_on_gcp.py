from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.storage import GCS
from diagrams.gcp.compute import AppEngine
from diagrams.onprem.client import User
from diagrams.generic.os import Ubuntu

with Diagram("Data Visualization App on GCP", show=False):
    user = User("User")

    with Cluster("GCP Services"):
        app_engine = AppEngine("Dash App")
        bigquery = BigQuery("BigQuery")
        cloud_storage = GCS("Cloud Storage")

    with Cluster("Local Development"):
        local_env = Ubuntu("Local Environment")

    user >> Edge(color="blue", style="dashed") >> local_env
    local_env >> Edge(label="Deploy", color="green") >> app_engine

    app_engine >> Edge(label="Load Data", color="orange") >> bigquery
    app_engine >> Edge(label="Load Data", color="orange") >> cloud_storage

    app_engine << Edge(color="red", style="dotted") >> user
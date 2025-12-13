from diagrams import Diagram, Cluster
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import BigQuery

with Diagram("AI Platform Training Job Notification Architecture", show=False):
    with Cluster("Google Cloud Platform"):
        # Core Services
        ai_platform = AIPlatform("AI Platform Training")
        log_topic = PubSub("Log Topic")
        notification_topic = PubSub("Notification Topic")
        cloud_function = Functions("Cloud Function")
        storage = Storage("Cloud Storage")
        logs = BigQuery("Cloud Logging")

        # Flow
        logs >> log_topic >> cloud_function
        cloud_function >> notification_topic
        ai_platform - storage
        ai_platform >> logs
from diagrams import Diagram
from diagrams.gcp.ml import AIPlatform, AIPlatformDataLabelingService
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import GCF
from diagrams.gcp.devtools import GCR
from diagrams.gcp.storage import GCS

with Diagram("Google AI Platform Training Job Notification", show=False):
    logs = AIPlatform("AI Platform Logs")
    log_sink = PubSub("Log Sink")
    cloud_function = GCF("Cloud Function")
    notification_topic = PubSub("Notification Topic")
    storage_bucket = GCS("Cloud Function Source Code")
    gcr = GCR("Container Registry")
    
    logs >> log_sink >> cloud_function
    cloud_function >> notification_topic
    gcr >> cloud_function
    storage_bucket >> cloud_function
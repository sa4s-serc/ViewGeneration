from diagrams import Diagram
from diagrams.gcp.storage import Storage
from diagrams.gcp.devtools import Functions
from diagrams.gcp.analytics import Logging
from diagrams.gcp.integration import PubSub

with Diagram("Google AI Platform Training Job Notification", show=False, direction="TB"):
    log_sink = Logging("Log Sink")
    ai_platform_logs = PubSub("AI Platform Log Topic")
    notification_topic = PubSub("Notification Topic")
    
    cloud_storage = Storage("Cloud Storage Bucket")
    cloud_function = Functions("Job State Detection Function")
    
    log_sink >> ai_platform_logs
    ai_platform_logs >> cloud_function
    cloud_function >> notification_topic
    cloud_function << cloud_storage
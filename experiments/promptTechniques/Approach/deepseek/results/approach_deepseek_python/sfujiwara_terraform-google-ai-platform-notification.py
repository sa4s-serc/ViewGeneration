from diagrams import Diagram
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.storage import Storage
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.operations import Logging

with Diagram("Google AI Platform Training Job Notification Module", show=False, direction="LR"):
    ai_platform = AIPlatform("AI Platform\nTraining Jobs")
    logging_sink = Logging("Logging Sink")
    log_topic = PubSub("AI Platform Log Topic")
    cloud_function = Functions("Cloud Function")
    notification_topic = PubSub("Notification Topic")
    
    ai_platform >> logging_sink >> log_topic >> cloud_function >> notification_topic
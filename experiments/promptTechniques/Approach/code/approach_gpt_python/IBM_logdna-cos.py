from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.ibm.cloud import Iam
from diagrams.ibm.analytics import Logdna
from diagrams.ibm.devops import Functions
from diagrams.ibm.storage import IbmCloudBlockStorage

with Diagram("Serverless Log Processing", show=False):
    client = Client("User")
    
    with Cluster("IBM Cloud"):
        cos_source = IbmCloudBlockStorage("COS Bucket (Source)")
        cos_archive = IbmCloudBlockStorage("COS Bucket (Archive)")
        
        with Cluster("Serverless Function"):
            handler = Functions("handler.js")
            log_retrieval = Functions("Log Retrieval")
            log_processing = Functions("Log Processing")
            log_forwarding = Functions("Log Forwarding")
            log_archiving = Functions("Log Archiving")
            error_handling = Functions("Error Handling")

        logdna = Logdna("LogDNA")
        
        client >> Edge(label="Trigger") >> cos_source
        cos_source >> Edge(label="New Object Event") >> handler
        handler >> Edge(label="Download Logs") >> log_retrieval
        log_retrieval >> Edge(label="Unzip & Parse") >> log_processing
        log_processing >> Edge(label="Batching & Send") >> log_forwarding
        log_forwarding >> Edge(label="API Call", style="dashed") >> logdna
        log_forwarding >> Edge(label="Retry on Failure", style="dotted") >> error_handling
        log_forwarding >> Edge(label="Archive Logs") >> log_archiving
        log_archiving >> Edge(label="Copy & Delete") >> cos_archive
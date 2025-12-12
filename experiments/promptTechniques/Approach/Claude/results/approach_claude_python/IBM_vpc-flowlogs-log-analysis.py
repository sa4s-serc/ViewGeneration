from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.network import VPC
from diagrams.ibm.general import MonitoringLogging

# Create architecture diagram
with Diagram("VPC Flow Log Processing Architecture", show=False):
    
    with Cluster("IBM Cloud"):
        log_analysis = MonitoringLogging("IBM Log Analysis")

    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            vpc = VPC("VPC")
            
        with Cluster("Storage & Processing"):
            receiver = S3("Receiver Bucket")
            archive = S3("Archive Bucket")
            
            function = Lambda("Processing Function")
            
        # Define dataflows
        vpc >> Edge(label="flow logs") >> receiver
        receiver >> Edge(label="trigger") >> function
        function >> Edge(label="archive") >> archive
        function >> Edge(label="forward logs") >> log_analysis
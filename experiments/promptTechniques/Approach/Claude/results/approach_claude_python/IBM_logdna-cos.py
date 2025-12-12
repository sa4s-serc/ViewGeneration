from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.generic.storage import Storage
from diagrams.aws.management import CloudwatchLogs

with Diagram("CIS Logs to LogDNA Architecture", show=False):
    with Cluster("IBM Cloud"):
        logdna = Storage("LogDNA")

    with Cluster("AWS Cloud"):
        source_bucket = S3("Source COS Bucket")
        archive_bucket = S3("Archive COS Bucket")
        logs = CloudwatchLogs("Logs")
        
        with Cluster("Serverless Processing"):
            function = Lambda("Log Processing Function")
        
        source_bucket >> function
        function >> logdna
        function >> archive_bucket
        function >> logs
from diagrams import Diagram
from diagrams.aws.storage import S3
from diagrams.ibm.applications import ActionableInsight
from diagrams.ibm.infrastructure import EdgeServices
from diagrams.ibm.storage import BlockStorage

with Diagram("Serverless Flow Log Processing Architecture", show=False):
    source_bucket = BlockStorage("COS Source Bucket")
    action = ActionableInsight("Flow Log Processing Function")
    log_analysis = EdgeServices("IBM Log Analysis")
    archive_bucket = S3("COS Archive Bucket")

    source_bucket >> action >> log_analysis
    action >> archive_bucket
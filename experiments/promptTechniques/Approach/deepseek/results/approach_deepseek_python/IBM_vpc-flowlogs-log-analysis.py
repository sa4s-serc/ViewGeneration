from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.network import VPCFlowLogs
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server

with Diagram("Serverless Flow Log Processing Architecture", show=False):
    vpc_flow_logs = VPCFlowLogs("VPC Flow Logs")
    cos_receiver = S3("COS Receiver Bucket")
    cos_archive = S3("COS Archive Bucket")
    log_analysis = ElasticsearchService("IBM Log Analysis")
    handler = Lambda("handler.js")
    index = Lambda("index.js")
    local_handler = Server("local-handler.js")
    user = User("Developer")

    vpc_flow_logs >> cos_receiver
    cos_receiver >> handler
    handler >> log_analysis
    handler >> cos_archive
    cos_receiver >> local_handler
    local_handler >> handler
    user >> index
    index >> handler
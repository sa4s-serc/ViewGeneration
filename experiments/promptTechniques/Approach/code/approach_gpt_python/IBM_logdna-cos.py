from diagrams import Diagram
from diagrams.ibm.applications import AppServer
from diagrams.ibm.general import Internet, CloudMessaging
from diagrams.ibm.management import CloudManagement
from diagrams.ibm.data import FileRepository
from diagrams.ibm.devops import ReleaseManagement
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.programming.flowchart import Decision, Collate, Action

with Diagram("IBM CIS Logs to LogDNA Serverless Function Architecture", show=False):
    internet = Internet("User")
    cloud_storage = S3("IBM COS Bucket")
    serverless_function = AppServer("Serverless Function")
    api_gateway = APIGateway("LogDNA API")
    cloud_management = CloudManagement("IBM Cloud Functions")
    log_analysis = CloudMessaging("LogDNA")
    archive_storage = FileRepository("Archive COS Bucket")
    cloudwatch = Cloudwatch("Monitoring & Logging")
    error_handling = Decision("Error Handling")
    log_processing = Collate("Log Processing")
    log_forwarding = Action("Log Forwarding")
    log_archiving = Action("Log Archiving")
    release_management = ReleaseManagement("Deployment")

    internet >> cloud_storage >> serverless_function
    serverless_function >> log_processing >> [log_forwarding, log_archiving]
    log_forwarding >> api_gateway >> log_analysis
    log_archiving >> archive_storage
    serverless_function >> error_handling >> cloudwatch
    release_management >> cloud_management >> serverless_function
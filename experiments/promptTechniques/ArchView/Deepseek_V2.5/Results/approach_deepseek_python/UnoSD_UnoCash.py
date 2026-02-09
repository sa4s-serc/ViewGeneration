from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.ml import Rekognition
from diagrams.aws.security import Cognito
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS

with Diagram("UnoCash Architecture", show=False, direction="TB"):
    with Cluster("Frontend"):
        blazor = Lambda("Blazor SPA")
    
    with Cluster("Backend Services"):
        api_gateway = APIGateway("API Gateway")
        
        with Cluster("Azure Functions"):
            functions = [
                Lambda("GetExpenses"),
                Lambda("AddExpense"),
                Lambda("UpdateExpense"),
                Lambda("DeleteExpense"),
                Lambda("GetReceiptData"),
                Lambda("GetReceiptUploadSasToken")
            ]
    
    with Cluster("Data Layer"):
        table_storage = Dynamodb("Azure Table Storage")
        blob_storage = S3("Azure Blob Storage")
    
    with Cluster("AI Services"):
        form_recognizer = Rekognition("Form Recognizer")
    
    with Cluster("Security"):
        auth = Cognito("Azure AD")
    
    with Cluster("Monitoring"):
        monitoring = Cloudwatch("Application Insights")
    
    with Cluster("Messaging"):
        queues = SQS("Event Queues")

    blazor >> api_gateway
    api_gateway >> functions
    functions >> table_storage
    functions >> blob_storage
    functions >> form_recognizer
    auth >> api_gateway
    functions >> monitoring
    functions >> queues
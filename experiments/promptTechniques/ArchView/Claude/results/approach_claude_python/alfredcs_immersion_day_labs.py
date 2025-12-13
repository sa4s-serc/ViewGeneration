from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import SagemakerModel, SagemakerNotebook, Sagemaker, Rekognition, Comprehend, Translate
from diagrams.aws.storage import S3
from diagrams.aws.database import DynamodbTable
from diagrams.aws.integration import StepFunctions
from diagrams.aws.security import Cognito

with Diagram("ML Workflow Architecture", show=False):
    with Cluster("Data Layer"):
        storage = S3("Data Storage")
        db = DynamodbTable("Metadata Store")

    with Cluster("ML Training & Processing"):
        notebook = SagemakerNotebook("Development")
        training = Sagemaker("Training")
        model = SagemakerModel("Model Hosting")

    with Cluster("ML Services"):
        rekognition = Rekognition("Computer Vision")
        comprehend = Comprehend("NLP")
        translate = Translate("Translation")

    with Cluster("Orchestration"):
        workflow = StepFunctions("Workflow")
        function = Lambda("Processing")

    auth = Cognito("Authentication")

    # Data flow
    storage >> notebook
    notebook >> training
    training >> model
    
    # Service integration
    model >> rekognition
    model >> comprehend
    model >> translate
    
    # Workflow orchestration
    workflow >> function
    function >> db
    
    # Security
    auth >> [notebook, function]
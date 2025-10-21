from diagrams import Diagram, Cluster
from diagrams.aws.ml import Sagemaker, SagemakerModel, SagemakerTrainingJob
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.security import IAM
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client

with Diagram("Amazon SageMaker ML Workflow", show=False, direction="TB"):
    client = Client("User")
    
    with Cluster("Data Handling and Preprocessing"):
        s3 = S3("Datasets")
        data_processing = Lambda("Data Processing")
        s3 >> data_processing

    with Cluster("Model Training"):
        training_job = SagemakerTrainingJob("Training Job")
        pre_trained_model = SagemakerModel("Pre-trained Model")
        data_processing >> training_job
        pre_trained_model >> training_job
    
    with Cluster("Model Deployment"):
        model_deployment = Sagemaker("Model Deployment")
        training_job >> model_deployment

    with Cluster("Governance and Security"):
        iam = IAM("IAM Policies")
        iam >> model_deployment
        iam >> data_processing
    
    client >> s3
    model_deployment >> client
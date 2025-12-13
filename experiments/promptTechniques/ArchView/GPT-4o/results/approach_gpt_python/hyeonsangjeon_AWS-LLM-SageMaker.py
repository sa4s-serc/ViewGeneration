from diagrams import Diagram
from diagrams.aws.ml import Sagemaker, SagemakerModel, SagemakerTrainingJob
from diagrams.aws.analytics import AmazonOpensearchService
from diagrams.onprem.analytics import Metabase
from diagrams.programming.language import Python
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.onprem.container import Docker

with Diagram("AWS LLM SageMaker Workshop and RAG Implementation", show=False):
    s3 = S3("Data Storage")
    sagemaker = Sagemaker("SageMaker")
    model_training = SagemakerTrainingJob("Model Training")
    model_deploy = SagemakerModel("Model Deployment")
    opensearch = AmazonOpensearchService("OpenSearch")
    faiss = Metabase("FAISS")
    docker = Docker("Streamlit UI")
    ec2 = EC2("EC2 Instance")
    python = Python("Python Code")

    s3 >> sagemaker >> model_training >> model_deploy
    model_deploy >> opensearch
    model_deploy >> faiss
    opensearch >> docker
    faiss >> docker
    docker << ec2
    ec2 >> python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.ml import Sagemaker, SagemakerGroundTruth
from diagrams.aws.database import Dynamodb
from diagrams.aws.analytics import OpenSearchService
from diagrams.onprem.client import Users
from diagrams.custom import Custom

with Diagram("AWS LLM SageMaker Workshop and RAG Architecture", show=False):
    user = Users("User")
    streamlit_ui = Custom("Streamlit UI", "./icons/streamlit.png")

    with Cluster("AWS SageMaker"):
        sagemaker_endpoint = Sagemaker("LLM Endpoint")
        sagemaker_training = SagemakerGroundTruth("Training")

    with Cluster("Amazon OpenSearch"):
        opensearch = OpenSearchService("Document Retriever")

    with Cluster("Inference Utilities"):
        prompter = Custom("Prompter", "./icons/prompter.png")
        kollm_endpoint = Custom("KoLLMSageMakerEndpoint", "./icons/kollm.png")

    with Cluster("Data Indexing and Embedding"):
        vector_embedding = Custom("Embedding Model", "./icons/embedding.png")
        faiss_search = Custom("FAISS Search", "./icons/faiss.png")

    user >> streamlit_ui
    streamlit_ui >> kollm_endpoint
    kollm_endpoint >> sagemaker_endpoint
    sagemaker_endpoint >> opensearch
    opensearch >> faiss_search
    faiss_search >> vector_embedding
    vector_embedding >> sagemaker_training
    sagemaker_training >> sagemaker_endpoint
    prompter >> sagemaker_endpoint
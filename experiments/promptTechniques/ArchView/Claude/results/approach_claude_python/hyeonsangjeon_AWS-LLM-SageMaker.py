from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway 
from diagrams.aws.analytics import OpenSearchService
from diagrams.custom import Custom

with Diagram("Korean Financial Q&A Chatbot Architecture", show=False):
    with Cluster("Data Layer"):
        s3 = S3("Document Storage")
        opensearch = OpenSearchService("Vector Store")
        
    with Cluster("Model Layer"):
        sagemaker = SagemakerModel("Korean LLM\n(KULLM-Polyglot)")
        embedding = SagemakerModel("Embedding Model")
    
    with Cluster("Application Layer"):
        api = APIGateway("API Gateway")
        rag_lambda = Lambda("RAG Logic")
        streamlit = Custom("Streamlit UI", "./streamlit.png")
        
    # Data flow
    s3 >> embedding >> opensearch
    api >> rag_lambda
    rag_lambda >> opensearch
    rag_lambda >> sagemaker
    streamlit >> api
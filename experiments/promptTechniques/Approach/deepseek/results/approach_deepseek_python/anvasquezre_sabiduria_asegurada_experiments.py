from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet
from diagrams.aws.storage import S3
from diagrams.programming.framework import FastAPI
from diagrams.aws.ml import Sagemaker

with Diagram("Policy Guru Chatbot Architecture", show=False):
    user = User("User")
    
    with Cluster("Frontend Layer"):
        chainlit = FastAPI("Chainlit Frontend")
    
    with Cluster("Application Layer"):
        with Cluster("Chatbot Application"):
            app = Server("app.py")
            agent_utils = Server("agent_utils.py")
            data_utils = Server("data_utils.py")
            config = Server("config.py")
            text_templates = Server("text_templates.py")
    
    with Cluster("Data Layer"):
        qdrant = MongoDB("Qdrant Vector DB")
        s3_storage = S3("S3 Storage")
    
    with Cluster("External Services"):
        google_search = Internet("Google Search API")
        langchain = Sagemaker("LangChain Agent")
    
    with Cluster("Data Preprocessing"):
        data_preloader = Server("Data Preloader")
        document_utils = Server("document_utils.py")
        data_preloader_config = Server("config.py")
        health_check = Server("health_check.py")
    
    user >> chainlit
    chainlit >> app
    app >> agent_utils
    app >> data_utils
    agent_utils >> langchain
    agent_utils >> google_search
    data_utils >> qdrant
    data_preloader >> s3_storage
    data_preloader >> qdrant
    document_utils >> data_preloader
    data_preloader_config >> data_preloader
    health_check >> data_preloader
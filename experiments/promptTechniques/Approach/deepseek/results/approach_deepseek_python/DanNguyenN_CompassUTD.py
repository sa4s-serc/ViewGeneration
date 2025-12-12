from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("CompassUTD Chatbot Architecture", show=False):
    user = User("User")
    
    with Cluster("API Layer"):
        api = EC2("FastAPI App")
    
    with Cluster("Inference Layer"):
        inference = EC2("CompassInference")
        llm = EC2("PaLM 2")
        langchain = EC2("Langchain")
    
    with Cluster("Tool Layer"):
        tools = [
            EC2("SearchCourse"),
            EC2("SearchDegree"),
            EC2("SearchGeneral"),
            EC2("DefinitionLookup"),
            EC2("RateMyProfessor")
        ]
    
    with Cluster("Web Scraping Layer"):
        webscrape = EC2("TextExtractor")
    
    with Cluster("Data Layer"):
        db = RDS("MongoDB")
    
    user >> ELB("Load Balancer") >> api
    api >> inference
    inference >> llm
    inference >> langchain
    langchain >> tools
    tools >> webscrape
    api >> db
    inference >> db
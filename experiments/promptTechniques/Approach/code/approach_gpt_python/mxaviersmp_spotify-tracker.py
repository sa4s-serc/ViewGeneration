from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Client
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python

with Diagram("Spotify Tracker Architecture", show=False):
    user = Client("User")

    with Cluster("Spotify Tracker"):
        with Cluster("API Layer"):
            api_gateway = APIGateway("API Gateway")
            lambda_function = Lambda("FastAPI")
            api_gateway >> Edge(label="REST API") >> lambda_function

        with Cluster("ETL Layer"):
            airflow = Airflow("Airflow DAG")
        
        with Cluster("Database Layer"):
            rds = RDS("PostgreSQL AWS RDS")
            local_pg = PostgreSQL("Local PostgreSQL")

        with Cluster("CI/CD"):
            github_actions = GithubActions("GitHub Actions")
        
        streamlit = Python("Streamlit App")

    user >> Edge(label="HTTP Request") >> api_gateway
    lambda_function >> Edge(label="DB Access") >> rds
    lambda_function >> Edge(label="DB Access") >> local_pg
    airflow >> Edge(label="ETL Process") >> rds
    github_actions >> Edge(label="Deployment & Migrations") >> lambda_function
    github_actions >> Edge(label="Deployment & Migrations") >> rds
    user >> Edge(label="UI Interaction") >> streamlit
    streamlit >> Edge(label="API Call") >> api_gateway
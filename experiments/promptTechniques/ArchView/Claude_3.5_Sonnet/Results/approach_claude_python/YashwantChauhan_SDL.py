from diagrams import Diagram, Cluster
from diagrams.programming.framework import Django
from diagrams.onprem.database import MySQL
from diagrams.onprem.queue import Rabbitmq
from diagrams.azure.ml import MachineLearningServiceWorkspaces  
from diagrams.aws.security import IAM
from diagrams.saas.identity import Auth0
from diagrams.azure.web import AppServiceEnvironments

with Diagram("SDL Intrusion Detection System Architecture", show=False):
    with Cluster("Web Layer"):
        web = Django("Django Web App")
        auth = Auth0("Authentication")

    with Cluster("Processing Layer"):
        ml = MachineLearningServiceWorkspaces("Random Forest\nClassifier")
        queue = Rabbitmq("Task Queue")

    with Cluster("Data Layer"):
        db = MySQL("Database")

    with Cluster("Security Layer"):
        iam = IAM("Access Control")
        
    with Cluster("Deployment"):
        app_service = AppServiceEnvironments("Heroku")

    # Flow
    web >> auth
    web >> queue
    queue >> ml
    ml >> db
    web >> iam
    web >> db
    web - app_service
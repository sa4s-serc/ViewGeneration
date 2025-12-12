from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.programming.framework import Angular
from diagrams.programming.framework import Spring
from diagrams.aws.database import Aurora
from diagrams.aws.blockchain import Blockchain
from diagrams.aws.integration import SNS
from diagrams.aws.security import IAM
from diagrams.aws.security import Cognito

with Diagram("LwM2M and Blockchain Architecture", show=False):
    with Cluster("Frontend"):
        angular_app = Angular("Anomaly Detection App")
        admin_app = Angular("Management App")

    with Cluster("Backend Services"):
        api = APIGateway("REST API")
        auth = Cognito("Authentication")
        iam = IAM("Access Control")
        
        with Cluster("Business Logic"):
            spring = Spring("Spring Boot Backend")
            lambda_fn = Lambda("Event Handlers")

    with Cluster("Storage"):
        db = Aurora("Database")
        blockchain = Blockchain("Ethereum Network")
        events = SNS("Event Bus")

    # Frontend to Backend
    angular_app >> api >> spring
    admin_app >> api >> spring

    # Auth Flow
    api >> auth
    auth >> iam

    # Backend Processing
    spring >> lambda_fn
    spring >> db
    spring >> blockchain
    lambda_fn >> events
    events >> blockchain
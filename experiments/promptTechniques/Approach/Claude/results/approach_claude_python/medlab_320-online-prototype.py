from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway, ELB
from diagrams.azure.database import CosmosDb
from diagrams.azure.compute import ContainerInstances
from diagrams.programming.framework import React
from diagrams.azure.identity import ActiveDirectory

with Diagram("MedLab Online Prototype Architecture", show=False):
    with Cluster("Frontend"):
        web = React("React Frontend")

    with Cluster("Backend Services"):
        api = APIGateway("API Gateway")
        auth = ActiveDirectory("Auth Service")
        containers = ContainerInstances("Microservices")
        db = CosmosDb("Database")

    with Cluster("Testing Infrastructure"):
        test = Lambda("Test Framework")

    # Frontend connections
    web >> api

    # Backend connections
    api >> auth
    api >> containers
    containers >> db

    # Testing connections
    test >> web
    test >> api
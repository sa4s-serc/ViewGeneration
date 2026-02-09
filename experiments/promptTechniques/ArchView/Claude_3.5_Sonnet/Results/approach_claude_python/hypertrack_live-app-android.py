from diagrams import Diagram, Cluster
from diagrams.aws.security import Cognito
from diagrams.firebase.develop import Authentication
from diagrams.gcp.compute import KubernetesEngine
from diagrams.programming.framework import React
from diagrams.onprem.database import MongoDB
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import S3
from diagrams.gcp.ml import AIHub

with Diagram("HyperTrack Live App Architecture", show=False):
    
    with Cluster("Frontend"):
        web = React("Mobile App")

    with Cluster("Authentication"):
        auth = Cognito("AWS Cognito")
        firebase_auth = Authentication("Firebase Auth")
        auth - firebase_auth

    with Cluster("Backend Services"):
        api = APIGateway("API Gateway")
        storage = S3("Storage")
        db = MongoDB("Database")
        location = AIHub("Location Services")

    with Cluster("Container Platform"):
        k8s = KubernetesEngine("Kubernetes")

    # Frontend connections
    web >> auth
    web >> api

    # Backend connections
    api >> k8s
    k8s >> db
    k8s >> storage
    k8s >> location
    auth >> api
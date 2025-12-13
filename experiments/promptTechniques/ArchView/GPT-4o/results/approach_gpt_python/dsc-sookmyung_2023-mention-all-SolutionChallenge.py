from diagrams import Diagram, Cluster, Edge
from diagrams.generic.os import Android, IOS
from diagrams.programming.language import Java
from diagrams.firebase.develop import Authentication
from diagrams.firebase.grow import ABTesting
from diagrams.gcp.ml import AIHub, AIPlatform, AIPlatformDataLabelingService
from diagrams.aws.mobile import APIGateway
from diagrams.gcp.storage import GCS
from diagrams.gcp.compute import AppEngine

with Diagram("CPR2U: An Integrated CPR Education and Emergency Response System", show=False):
    with Cluster("Mobile Applications"):
        android_app = Android("Android Application (Kotlin)")
        ios_app = IOS("iOS Application (Swift)")

    with Cluster("Backend"):
        spring_boot_backend = Java("Spring Boot Backend")
        authentication = Authentication("JWT Tokens")
        api_gateway = APIGateway("REST API Communication")
        firebase_cloud_messaging = ABTesting("Firebase Cloud Messaging")

    with Cluster("GCP Deployment"):
        app_engine = AppEngine("Google Cloud App Engine")
        ai_platform = AIPlatform("TensorFlow Lite")
        ai_data_labeling = AIPlatformDataLabelingService("Data Labeling")
        ai_hub = AIHub("AI Hub")

    android_app >> Edge(label="Pose Estimation") >> ai_platform
    ios_app >> Edge(label="Pose Estimation") >> ai_platform

    android_app >> Edge(label="Firebase Integration") >> firebase_cloud_messaging
    ios_app >> Edge(label="Firebase Integration") >> firebase_cloud_messaging

    android_app >> Edge(label="Authentication") >> authentication
    ios_app >> Edge(label="Authentication") >> authentication

    spring_boot_backend >> Edge(label="API Communication") >> api_gateway
    api_gateway >> Edge(label="Dispatch System") >> firebase_cloud_messaging

    android_app >> Edge(label="Location Tracking") >> app_engine
    ios_app >> Edge(label="Location Tracking") >> app_engine

    app_engine >> Edge(label="Deployment") >> spring_boot_backend
    spring_boot_backend >> Edge(label="Certification Progress") >> ai_data_labeling

    with Cluster("Data Storage"):
        gcs = GCS("Google Cloud Storage")
        spring_boot_backend >> Edge(label="Stores Data") >> gcs
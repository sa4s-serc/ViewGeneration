from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.firebase.develop import Authentication, RealtimeDatabase
from diagrams.gcp.compute import GKE
from diagrams.gcp.storage import GCS
from diagrams.gcp.devtools import ContainerRegistry
from diagrams.gcp.ml import AIPlatform
from diagrams.programming.language import Kotlin, Swift, Java
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.google.maps import Maps
from diagrams.firebase.gcp import Firestore

with Diagram("CPR2U: Integrated CPR Education and Emergency Response System", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Mobile Applications"):
        android_app = Custom("Android App", "./path-to-android-icon.png")  # Custom icon path for Android
        ios_app = Custom("iOS App", "./path-to-ios-icon.png")  # Custom icon path for iOS
        
        with Cluster("Android Modules"):
            ml_kit = AIPlatform("ML Kit (TensorFlow Lite)")
            firebase_auth = Authentication("Firebase Auth")
            firebase_db = RealtimeDatabase("Firebase Realtime DB")
            firebase_messaging = Firestore("Firebase Cloud Messaging")
            google_maps_android = Maps("Google Maps API")
        
        with Cluster("iOS Modules"):
            ios_ml = AIPlatform("TensorFlow Lite")
            ios_maps = Maps("Google Maps API")
    
    with Cluster("Backend Services"):
        server = Server("Spring Boot Backend")
        auth_service = Java("AuthService.java")
        education_service = Java("EducationProgressService.java")
        dispatch_service = Java("DispatchService.java")
        firebase_util = Java("FirebaseCloudMessageUtil.java")
        address_service = Java("AddressService.java")
    
    user >> android_app >> [ml_kit, firebase_auth, firebase_db, firebase_messaging, google_maps_android]
    user >> ios_app >> [ios_ml, ios_maps]
    
    android_app >> server
    ios_app >> server
    
    with Cluster("Deployment"):
        gke = GKE("Google Kubernetes Engine")
        gcs = GCS("Google Cloud Storage")
        container_registry = ContainerRegistry("Container Registry")
        
        server >> gke
        server >> gcs
        server >> container_registry
    
    server >> auth_service
    server >> education_service
    server >> dispatch_service
    server >> firebase_util
    server >> address_service